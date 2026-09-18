-- ============================================================
-- INSERT new videos
-- ============================================================

INSERT INTO core.youtube_videos (
    video_id,
    title,
    published_at,
    duration_seconds,
    view_count,
    like_count,
    comment_count
)
SELECT
    video_id,
    title,
    published_at,

    (
        COALESCE(
            substring(duration FROM '([0-9]+)H')::INTEGER,
            0
        ) * 3600
        +
        COALESCE(
            substring(duration FROM '([0-9]+)M')::INTEGER,
            0
        ) * 60
        +
        COALESCE(
            substring(duration FROM '([0-9]+)S')::INTEGER,
            0
        )
    ) AS duration_seconds,

    view_count,
    like_count,
    comment_count

FROM staging.youtube_videos

WHERE video_id NOT IN (
    SELECT video_id
    FROM core.youtube_videos
);


-- ============================================================
-- UPDATE existing videos
-- ============================================================

UPDATE core.youtube_videos AS core

SET
    title = staging.title,
    published_at = staging.published_at,

    duration_seconds =
        COALESCE(
            substring(staging.duration FROM '([0-9]+)H')::INTEGER,
            0
        ) * 3600
        +
        COALESCE(
            substring(staging.duration FROM '([0-9]+)M')::INTEGER,
            0
        ) * 60
        +
        COALESCE(
            substring(staging.duration FROM '([0-9]+)S')::INTEGER,
            0
        ),

    view_count = staging.view_count,
    like_count = staging.like_count,
    comment_count = staging.comment_count,

    loaded_at = CURRENT_TIMESTAMP

FROM staging.youtube_videos AS staging

WHERE core.video_id = staging.video_id;


-- ============================================================
-- DELETE videos that no longer exist in staging
-- ============================================================

DELETE FROM core.youtube_videos

WHERE video_id NOT IN (
    SELECT video_id
    FROM staging.youtube_videos
);