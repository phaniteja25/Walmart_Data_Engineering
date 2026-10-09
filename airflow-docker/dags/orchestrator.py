from airflow.sdk import dag,task
from airflow.operators.bash import BashOperator
from databricks.sdk import WorkspaceClient
import os
import time
from databricks.sdk.service.jobs import RunResultState

@dag()
def orchestrator():
    
    @task()
    def ingest_cdc():
        w = WorkspaceClient()  # reads DATABRICKS_HOST / DATABRICKS_TOKEN from env
        run = w.jobs.run_now(job_id=int(os.environ["DATABRICKS_JOB_ID"])).result()  # blocks until the run finishes
        if run.state.result_state != RunResultState.SUCCESS:
            raise Exception(f"Job failed: {run.state.result_state}")
        print("Job succeeded")
        
        

    
    @task.bash()
    def source_freshness():
        return "cd /opt/airflow/Walmart_dbt/walmart_proj_dbt && dbt source freshness"
    
    silver_technical = BashOperator(
        task_id="silver_technical",
        bash_command="cd /opt/airflow/Walmart_dbt/walmart_proj_dbt && dbt run --select silver_t"
    )
    
    
    silver_technical_tests = BashOperator(
        task_id="silver_technical_tests",
        bash_command="cd /opt/airflow/Walmart_dbt/walmart_proj_dbt && dbt test --select silver_t"
    )
    
    silver_business = BashOperator(
        task_id="silver_business",
        bash_command="cd /opt/airflow/Walmart_dbt/walmart_proj_dbt && dbt run --select silver_b"
    )
    
    silver_business_tests = BashOperator(
        task_id="silver_business_tests",
        bash_command="cd /opt/airflow/Walmart_dbt/walmart_proj_dbt && dbt test --select silver_b"
    )
    
    gold_ephemeral = BashOperator(
        task_id="gold_ephemeral",
        cwd = "/opt/airflow/Walmart_dbt/walmart_proj_dbt",
        bash_command="dbt run --select gold/ephemeral"
    )
    
    gold_dimensions = BashOperator(
        task_id="gold_dimensions",
        cwd = "/opt/airflow/Walmart_dbt/walmart_proj_dbt",
        bash_command="dbt snapshot"
    )
    
    gold_fact = BashOperator(
        task_id="gold_fact",
        cwd = "/opt/airflow/Walmart_dbt/walmart_proj_dbt",
        bash_command="dbt run --select gold"
    )
    
    ingest_cdc() >> source_freshness() >> silver_technical >> silver_technical_tests >> silver_business >> silver_business_tests >> gold_ephemeral >> gold_dimensions >> gold_fact


orchestrator()

