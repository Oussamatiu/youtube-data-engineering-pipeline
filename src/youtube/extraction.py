def get_channel(youtube, handle):
    response = youtube.channels().list(
        part=["contentDetails" ],
        forHandle=handle
    ).execute()

    if not response.get("items"):
        raise ValueError(f"Channel not found: {handle}")

    channel = response["items"][0]

    print("Uploads Playlist ID:", channel["contentDetails"]["relatedPlaylists"]["uploads"])
    return {
        "channel_id": channel["id"],
        "uploads_playlist_id": channel["contentDetails"]["relatedPlaylists"]["uploads"]
    }


def get_video_ids(youtube, uploads_playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            video_ids.append(
                item["contentDetails"]["videoId"]
            )

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids


def get_video_details(youtube, video_ids):
    videos = []

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i + 50]

        response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(batch)
        ).execute()

        videos.extend(response.get("items", []))

    return videos


def extract_channel_videos(youtube, handle):
    channel = get_channel(youtube, handle)

    video_ids = get_video_ids(
        youtube,
        channel["uploads_playlist_id"]
    )

    print(f"Number of video IDs: {len(video_ids)}")

    videos = get_video_details(
        youtube,
        video_ids
    )

    print(f"Number of video details: {len(videos)}")

    return videos