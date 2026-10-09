from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="hello_world",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    BashOperator(task_id="say_hello", bash_command="echo 'Hello from Airflow!'")