from airflow import DAG
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from datetime import datetime, timedelta

# Define your DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    's3_to_hdfs_on_emr',
    default_args=default_args,
    description='Read JSON data from S3 and write it to HDFS on existing EMR cluster',
    schedule_interval='@hourly', 
)

# Define your EMR steps
emr_steps = [
    {
        'Name': 'Read JSON from S3 and write to HDFS',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                's3://myprojectemr/sparkscript/s3_to_hdfs.py',  # Adjust to your Spark application
                's3://myprojectemr/myinputfolder/tweets.json',  # Adjust to your S3 input path
                'hdfs://ip-10-0-11-178/outputdata/'  # Adjust to your HDFS output path
            ]
        }
    }
]

# Add steps to the existing EMR cluster
add_step_task = EmrAddStepsOperator(
    task_id='add_step_to_emr_cluster',
    job_flow_id='j-E65C9OZZ8BJF',  # Adjust to your EMR cluster ID
    aws_conn_id='aws_default',  # Your AWS connection ID
    steps=emr_steps,
    dag=dag,
)

# Define sensor to wait for the EMR step to complete
step_sensor_task = EmrStepSensor(
    task_id='watch_step',
    job_flow_id='j-E65C9OZZ8BJF',  # Adjust to your EMR cluster ID
    step_id="{{ task_instance.xcom_pull(task_ids='add_step_to_emr_cluster', key='return_value')[0] }}",
    aws_conn_id='aws_default',  # Your AWS connection ID
    dag=dag,
)

add_step_task >> step_sensor_task
