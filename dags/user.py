from airflow.sdk import asset, Asset
from click import Context

# Here we give an example of assets

@asset(
   schedule="@daily",
   uri="https://jsonplaceholder.typicode.com/users", 
)
def user(self) -> dict[str]:
    import requests
    # Access the URI from the asset context
    response = requests.get(self.uri)
    return response.json()[0]  # Returns the first user object


@asset.multi(
   schedule=user,
   outlets=[
      Asset(name="user_company"),
      Asset(name="user_address"),
   ]
)
def user_info(user: Asset, context: Context) -> list[dict[str]]:
   user_data = context['ti'].xcom_pull(
      dag_id=user.name, 
      task_ids=user.name, 
      include_prior_dates=True,
   )
   return [
      user_data['company'],
      user_data['address'],
   ]