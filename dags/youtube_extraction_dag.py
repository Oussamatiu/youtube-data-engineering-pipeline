from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from src.youtube.extraction_pipeline import (
    retrieve_channel,
    retrieve_video_ids,
    retrieve_video_details,
    parse_video_data,
    generate_json,
)


with DAG(
    dag_id="youtube_extraction",
    start_date=datetime(2026, 9, 15),
    schedule='@daily',
    catchup=False,
) as dag:

    retrieve_channel_task = PythonOperator(
        task_id="retrieve_channel",
        python_callable=retrieve_channel,
    )

    retrieve_video_ids_task = PythonOperator(
        task_id="retrieve_video_ids",
        python_callable=retrieve_video_ids,
        op_args=["{{ ti.xcom_pull(task_ids='retrieve_channel') }}"],
    )

    retrieve_video_details_task = PythonOperator(
        task_id="retrieve_video_details",
        python_callable=retrieve_video_details,
        op_args=["{{ ti.xcom_pull(task_ids='retrieve_video_ids') }}"],
    )

    parse_video_data_task = PythonOperator(
        task_id="parse_video_data",
        python_callable=parse_video_data,
        op_args=["{{ ti.xcom_pull(task_ids='retrieve_video_details') }}"],
    )

    generate_json_task = PythonOperator(
        task_id="generate_json",
        python_callable=generate_json,
        op_args=["{{ ti.xcom_pull(task_ids='parse_video_data') }}"],
    )

    trigger_warehouse_update = TriggerDagRunOperator(
        task_id="trigger_warehouse_update",
        trigger_dag_id="warehouse_update",
        wait_for_completion=False,
    )

    (
        retrieve_channel_task
        >> retrieve_video_ids_task
        >> retrieve_video_details_task
        >> parse_video_data_task
        >> generate_json_task
        >> trigger_warehouse_update
    )