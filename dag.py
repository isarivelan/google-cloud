"""A liveness prober dag for monitoring composer.googleapis.com/environment/healthy."""
import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2025, 1, 1),
    'depends_on_past': False,
    'email': ['misarivelan@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

dag = DAG('emp_data', 
          default_args=default_args,
          description='Runs as external Python script',
          schedule_interval='@daily',
          catchup=False)

with dag:
    run_script_task = BashOperator(
        task_id = 'extract_data',
        bash_command = 'python /home/airflow/gcs/dags/scripts/extract.py',
    )

    start_pipeline = CloudDataFusionStartPipelineOperator(
    location="us-central1",
    pipeline_name="etl-pipeline",
    instance_name="datafusion-2025",
    pipeline_timeout=1000,
    task_id="start_pipeline",
)
    run_script_task >> start_pipeline