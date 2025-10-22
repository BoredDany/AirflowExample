from airflow.sdk import task, dag

@dag
def sql_dag():
    
    @task.sql(
        conn_id = "postgres"
    )
    def get_nb_xcoms():
        return "SELECT COUNT(*) FROM xcom"
    
    get_nb_xcoms()

sql_dag()