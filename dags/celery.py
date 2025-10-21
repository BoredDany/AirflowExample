from airflow.sdk import dag, task
from time import sleep

@dag
def celery_dag():
    
    @task
    # Using celery executor, you can choose which queue to send the task to with the `queue` parameter
    def a():
        sleep(5)
        
    @task
    def b():
        sleep(5)

    @task
    def c():
        sleep(5)
        
    @task
    def d():
        sleep(5)
        
    a() >> [b(), c()] >> d()
    

celery_dag()