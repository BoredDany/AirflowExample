from airflow.sdk import dag, task, Context
from typing import Dict, Any

# This DAG is for giving an example of sharing xcoms between tasks

@dag
def xcom_dag():
    
    @task
    def t1() -> Dict[str, Any]:
        val = 42
        sentence = "Hello, World!"
        return {
            "val": val,
            "sentence": sentence
        }
    
    @task
    def t2(data: Dict[str, Any]):
        print(data["val"])
        print(data["sentence"])
    
    
    val = t1()
    t2(val)
    
xcom_dag()