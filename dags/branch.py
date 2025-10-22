from airflow.sdk import dag, task

# This DAG is for demonstrating how to do branching

@dag()

def branching_dag():
    
    @task()
    def a() -> int:
        return 1

    @task.branch()
    def b(val: int):
        if val == 1:
            return "equal_1"
        return "different_than_1"

    @task()
    def equal_1():
        print("Equal to 1")

    @task()
    def different_than_1():
        print("Not equal to 1")

    val = a()
    b(val) >> [equal_1(), different_than_1()]
    
    
branching_dag()