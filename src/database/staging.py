import json


def load_staging(connection, json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        videos = json.load(file)

    query = """
        INSERT INTO staging.youtube_videos (
            video_id,
            title,
            published_at,
            duration,
            view_count,
            like_count,
            comment_count
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (video_id)
        DO UPDATE SET
            title = EXCLUDED.title,
            published_at = EXCLUDED.published_at,
            duration = EXCLUDED.duration,
            view_count = EXCLUDED.view_count,
            like_count = EXCLUDED.like_count,
            comment_count = EXCLUDED.comment_count,
            loaded_at = CURRENT_TIMESTAMP;
    """

    with connection.cursor() as cursor:
        for video in videos:
            cursor.execute(
                query,
                (
                    video["videoId"],
                    video["title"],
                    video["publishedAt"],
                    video["duration"],
                    int(video.get("viewCount", 0)),
                    int(video.get("likeCount", 0)),
                    int(video.get("commentCount", 0))
                )
            )

    connection.commit()

    return len(videos)

def get_staging_data(connection):

    query = """
        SELECT
            video_id,
            title,
            published_at,
            duration,
            view_count,
            like_count,
            comment_count
        FROM staging.youtube_videos;
    """

    with connection.cursor() as cursor:

        cursor.execute(query)

        return cursor.fetchall()