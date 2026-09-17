import os
from pathlib import Path

from dotenv import load_dotenv

from src.database.connection import get_connection
from src.database.staging import load_staging
from src.database.core import load_core


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")



data_directory = PROJECT_ROOT / "data"

json_files = sorted(data_directory.glob("YTdata*.json"))

if not json_files:
    raise FileNotFoundError(
        "No YTdata*.json file found in the data folder."
    )

json_file = json_files[-1]

print(f"JSON file: {json_file}")



connection = get_connection()

try:

    staging_count = load_staging(
        connection,
        json_file
    )

    print(
        f"Rows loaded into staging: {staging_count}"
    )


    core_count = load_core(connection)

    print(
        f"Rows loaded into core: {core_count}"
    )


    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(*) FROM staging.youtube_videos;"
        )

        staging_rows = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM core.youtube_videos;"
        )

        core_rows = cursor.fetchone()[0]

    print(f"Staging rows: {staging_rows}")
    print(f"Core rows: {core_rows}")

 
    if staging_rows == 0:
        raise ValueError(
            "Staging table is empty."
        )

    if core_rows == 0:
        raise ValueError(
            "Core table is empty."
        )

    print("Database test completed successfully.")

finally:
    connection.close()