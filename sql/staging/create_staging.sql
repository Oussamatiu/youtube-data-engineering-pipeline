CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.youtube_videos (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    published_at TIMESTAMP,
    duration TEXT,
    view_count BIGINT,
    like_count BIGINT,
    comment_count BIGINT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
).