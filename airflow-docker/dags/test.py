from databricks.sdk import WorkspaceClient
import os
import time
from databricks.sdk.service.jobs import RunResultState

w = WorkspaceClient()  # reads DATABRICKS_HOST / DATABRICKS_TOKEN from env


run = w.jobs.run_now(job_id=int(os.environ["DATABRICKS_JOB_ID"])).result()  # blocks until the run finishes
if run.state.result_state != RunResultState.SUCCESS:
    raise Exception(f"Job failed: {run.state.result_state}")
print("Job succeeded")
        