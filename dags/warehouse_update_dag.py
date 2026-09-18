from datetime import datetime
from pathlib import Path
import json

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.connection import get_connection
from src.database.staging import load_staging, get_staging_data
from src.database.core import load_core
from src.transformations.transform import duration_to_seconds


PROJECT_ROOT = Path("/opt/airflow")
DATA_DIRECTORY = PROJECT_ROOT / "data"


def read_json():

    json_files = sorted(
        DATA_DIRECTORY.glob("YTdata*.json")
    )

    if not json_files:
        raise FileNotFoundError(
            "No YouTube JSON file found."
        )

    json_file = json_files[-1]

    print(f"Reading JSON file: {json_file}")

    with open(json_file, "r", encoding="utf-8") as file:
        videos = json.load(file)

    print(f"Number of videos: {len(videos)}")

    return str(json_file)


def update_staging(**context):

    json_file = context["ti"].xcom_pull(
        task_ids="read_json"
    )

    connection = get_connection()

    try:
        count = load_staging(
            connection,
            json_file
        )

        print(
            f"{count} videos loaded into staging."
        )

    finally:
        connection.close()


def transform_data():

    connection = get_connection()

    try:
        videos = get_staging_data(connection)

        transformed_videos = []

        for video in videos:

            transformed_videos.append(
                (
                    video[0],
                    video[1],
                    video[2],
                    duration_to_seconds(video[3]),
                    video[4],
                    video[5],
                    video[6],
                )
            )

        print(
            f"{len(transformed_videos)} videos transformed."
        )

        return transformed_videos

    finally:
        connection.close()


def update_core(**context):

    transformed_videos = context["ti"].xcom_pull(
        task_ids="transform_data"
    )

    connection = get_connection()

    try:
        count = load_core(
            connection,
            transformed_videos
        )

        print(
            f"{count} videos synchronized with core."
        )

    finally:
        connection.close()


with DAG(
    dag_id="warehouse_update",
    start_date=datetime(2026, 9, 1),
    schedule=None,
    catchup=False,
    tags=["youtube", "warehouse"],
) as dag:

    read_json_task = PythonOperator(
        task_id="read_json",
        python_callable=read_json,
    )

    update_staging_task = PythonOperator(
        task_id="update_staging",
        python_callable=update_staging,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    update_core_task = PythonOperator(
        task_id="update_core",
        python_callable=update_core,
    )

    (
        read_json_task
        >> update_staging_task
        >> transform_task
        >> update_core_task
    )