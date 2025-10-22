from airflow.sdk import dag, task, task_group

# This DAG is for giving an example of grouping tasks

@dag
def group():
    @task
    def a():
        return 42
        
    @task_group(
        default_args={
            "retries": 2
        }
    )
    def my_group(val: int):
        @task
        def b(my_val: int):
            print(my_val + 42)
            
        @task_group(
            default_args={
            "retries": 3
            }
        )
        def nested_group():
            @task
            def c():
                print("Task C executed")
            
            c()
                
        b(val) >> nested_group()

    val = a()
    my_group(val)
    
    
group()