import os
from pathlib import Path

from dotenv import load_dotenv

from src.youtube.api import create_youtube_client
from src.youtube.extraction import extract_channel_videos
from src.youtube.parser import parse_videos
from src.youtube.writer import save_videos_to_json


def extract_youtube_data():

    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    load_dotenv(PROJECT_ROOT / ".env")

    API_KEY = os.getenv("API_KEY")
    CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")

    if not API_KEY:
        raise ValueError("API_KEY is missing from .env")

    if not CHANNEL_HANDLE:
        raise ValueError("CHANNEL_HANDLE is missing from .env")

    youtube = create_youtube_client(API_KEY)

    videos = extract_channel_videos(
        youtube,
        CHANNEL_HANDLE
    )

    print(
        f"Number of videos extracted: {len(videos)}"
    )

    parsed_videos = parse_videos(videos)

    print(
        f"Number of videos parsed: {len(parsed_videos)}"
    )

    output_file = save_videos_to_json(
        parsed_videos,
        PROJECT_ROOT / "data"
    )

    print(f"JSON file created: {output_file}")

    for video in parsed_videos[:2]:
        print(video)

    return output_file


