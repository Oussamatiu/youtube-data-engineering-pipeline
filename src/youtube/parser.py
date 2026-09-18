def parse_video(video):
    snippet = video.get("snippet", {})
    content_details = video.get("contentDetails", {})
    statistics = video.get("statistics", {})

    return {
        "videoId": video.get("id"),
        "title": snippet.get("title"),
        "publishedAt": snippet.get("publishedAt"),
        "duration": content_details.get("duration"),
        "viewCount": statistics.get("viewCount", "0"),
        "likeCount": statistics.get("likeCount", "0"),
        "commentCount": statistics.get("commentCount", "0")
    }


def parse_videos(videos):
    return [
        parse_video(video)
        for video in videos
    ]