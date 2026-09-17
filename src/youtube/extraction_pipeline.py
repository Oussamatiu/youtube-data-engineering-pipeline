import json
import os
from pathlib import Path

from src.youtube.api import create_youtube_client
from src.youtube.extraction import (
    get_channel,
    get_video_ids,
    get_video_details,
)
from src.youtube.parser import parse_videos
from src.youtube.writer import save_videos_to_json


PROJECT_ROOT = Path("/opt/airflow")
DATA_DIR = PROJECT_ROOT / "data"


def get_youtube_client():
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY is missing")

    return create_youtube_client(api_key)


def retrieve_channel():
    youtube = get_youtube_client()

    channel_handle = os.getenv("CHANNEL_HANDLE")

    if not channel_handle:
        raise ValueError("CHANNEL_HANDLE is missing")

    channel = get_channel(
        youtube,
        channel_handle
    )

    channel_file = DATA_DIR / "channel.json"

    with open(channel_file, "w", encoding="utf-8") as file:
        json.dump(channel, file, ensure_ascii=False, indent=2)

    return str(channel_file)


def retrieve_video_ids(channel_file):
    youtube = get_youtube_client()

    with open(channel_file, "r", encoding="utf-8") as file:
        channel = json.load(file)

    video_ids = get_video_ids(
        youtube,
        channel["uploads_playlist_id"]
    )

    video_ids_file = DATA_DIR / "video_ids.json"

    with open(video_ids_file, "w", encoding="utf-8") as file:
        json.dump(video_ids, file, indent=2)

    print(f"Number of video IDs: {len(video_ids)}")

    return str(video_ids_file)


def retrieve_video_details(video_ids_file):
    youtube = get_youtube_client()

    with open(video_ids_file, "r", encoding="utf-8") as file:
        video_ids = json.load(file)

    videos = get_video_details(
        youtube,
        video_ids
    )

    details_file = DATA_DIR / "video_details.json"

    with open(details_file, "w", encoding="utf-8") as file:
        json.dump(videos, file, ensure_ascii=False, indent=2)

    print(f"Number of videos: {len(videos)}")

    return str(details_file)


def parse_video_data(video_details_file):
    with open(video_details_file, "r", encoding="utf-8") as file:
        videos = json.load(file)

    parsed_videos = parse_videos(videos)

    parsed_file = DATA_DIR / "parsed_videos.json"

    with open(parsed_file, "w", encoding="utf-8") as file:
        json.dump(
            parsed_videos,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"Number of parsed videos: {len(parsed_videos)}")

    return str(parsed_file)


def generate_json(parsed_file):
    with open(parsed_file, "r", encoding="utf-8") as file:
        parsed_videos = json.load(file)

    output_file = save_videos_to_json(
        parsed_videos,
        DATA_DIR
    )

    print(f"JSON generated: {output_file}")

    return str(output_file)