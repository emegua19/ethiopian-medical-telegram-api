from sqlalchemy import text
from sqlalchemy.orm import Session
from .schemas import Message, Detection, ChannelActivity

def search_messages(db: Session, query_str: str) -> list[Message]:
    sql = text("""
        SELECT
            message_id,
            message_text AS text,
            message_date AS date,
            file_path,
            channel
        FROM dbt_telegram_staging.stg_telegram_messages
        WHERE message_text ILIKE :q
        LIMIT 20
    """)
    rows = db.execute(sql, {"q": f"%{query_str}%"}).mappings().all()
    return [Message(**row) for row in rows]

def get_top_detections(db: Session, limit: int) -> list[Detection]:
    sql = text("""
        SELECT
            message_id,
            channel,  -- ✅ FIXED: was channel_name
            detected_class AS class_name,
            detection_confidence AS confidence
        FROM dbt_telegram_marts.fct_image_detections
        ORDER BY detection_confidence DESC
        LIMIT :limit
    """)
    rows = db.execute(sql, {"limit": limit}).mappings().all()
    return [Detection(**row) for row in rows]


def get_channel_activity(db: Session, channel: str) -> ChannelActivity:
    sql = text("""
        SELECT
            channel_id AS channel,
            COUNT(*) AS total_messages,
            MIN(message_date) AS first_post_date,
            MAX(message_date) AS last_post_date
        FROM dbt_telegram_marts.fct_messages
        WHERE channel_id = :channel
        GROUP BY channel_id
    """)
    row = db.execute(sql, {"channel": channel}).mappings().first()
    if not row:
        return ChannelActivity(
            channel=channel,
            total_messages=0,
            first_post_date=None,
            last_post_date=None
        )
    return ChannelActivity(**row)
