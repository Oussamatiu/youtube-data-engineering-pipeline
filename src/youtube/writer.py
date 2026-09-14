import json
from datetime import datetime
from pathlib import Path


def save_videos_to_json(videos, output_directory):
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")

    output_file = output_directory / f"YTdata{date}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            videos,
            file,
            ensure_ascii=False,
            indent=4
        )

    return output_file