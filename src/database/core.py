def load_core(connection, data):
    query = """
        INSERT INTO core.youtube_videos (
            video_id, title, published_at, duration_seconds,
            view_count, like_count, comment_count
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (video_id)
        DO UPDATE SET
            title = EXCLUDED.title,
            published_at = EXCLUDED.published_at,
            duration_seconds = EXCLUDED.duration_seconds,
            view_count = EXCLUDED.view_count,
            like_count = EXCLUDED.like_count,
            comment_count = EXCLUDED.comment_count,
            loaded_at = CURRENT_TIMESTAMP;
    """

    if not data:
        return 0

    with connection.cursor() as cursor:
        cursor.executemany(query, data)

    connection.commit()
    return len(data)