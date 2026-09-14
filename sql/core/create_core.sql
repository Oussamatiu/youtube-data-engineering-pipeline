CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.youtube_videos (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    published_at TIMESTAMP,
    duration_seconds INTEGER,
    view_count BIGINT,
    like_count BIGINT,
    comment_count BIGINT,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);