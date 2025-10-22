from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.postgres.hooks.postgres import PostgresHook

# This dags is an example of a process to get info from an api and save it in our db

@dag
def user_processing():
    
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres",
        sql="""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            firstname VARCHAR(255),
            lastname VARCHAR(255),
            email VARCHAR(255),
            city VARCHAR(255),
            phone VARCHAR(50),
            website VARCHAR(255),
            company VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Check condition every 30 seconds, and after 300 seconds the sensor fails if the condition is still false
    @task.sensor(poke_interval=30, timeout=300)
    def is_api_available():
        import requests
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        print(response.status_code)

        if response.status_code == 200:
            condition = True
            fake_users = response.json()
        else:
            condition = False
            fake_users = None

        return PokeReturnValue(is_done=condition, xcom_value=fake_users)

    @task
    def extract_user(fake_users):
        
        if not fake_users:
            raise ValueError("No users available from API")
    
        first = fake_users[0]
        firstname, *rest = first.get("name", "").split()
        lastname = " ".join(rest) if rest else ""
        user_row = {
            "id": first.get("id"),
            "firstname": firstname,
            "lastname": lastname,
            "email": first.get("email"),
            "city": first.get("address", {}).get("city"),
            "phone": first.get("phone"),
            "website": first.get("website"),
            "company": first.get("company", {}).get("name"),
        }
        print(user_row)
        return user_row
    
    @task
    def save_user_csv(user_info):
        import csv
        from datetime import datetime
        
        user_info["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("/tmp/user_info.csv", "w", newline="") as file:
            fieldnames = ["id", "firstname", "lastname", "email", "city", "phone", "website", "company", "created_at"]
            writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerow(user_info)
            
    @task
    def store_user():
        hook = PostgresHook(postgres_conn_id="postgres")
        hook.copy_expert(
            sql="COPY users (id, firstname, lastname, email, city, phone, website, company, created_at) FROM STDIN WITH CSV HEADER",
            filename="/tmp/user_info.csv"
        )

    save_user_csv(extract_user(create_table >> is_api_available())) >> store_user()
    
user_processing()