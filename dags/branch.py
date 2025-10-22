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
    def equal_1(val: int):
        print(f"Equal to 1: {val}")

    @task()
    def different_than_1(val: int):
        print(f"Not equal to 1: {val}")

    val = a()
    b(val) >> [equal_1(val), different_than_1(val)]
    
    
branching_dag()