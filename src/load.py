import os
import json
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'telegram_data')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD')

# === Connect to PostgreSQL ===
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cursor = conn.cursor()

# === Drop table with CASCADE to remove dbt views too ===
cursor.execute("DROP TABLE IF EXISTS raw.telegram_messages CASCADE;")
conn.commit()

# === Create schema and table ===
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cursor.execute("""
    CREATE TABLE raw.telegram_messages (
        id SERIAL PRIMARY KEY,
        message_id INTEGER,
        date TIMESTAMP,
        text TEXT,
        channel VARCHAR(255),
        file_path VARCHAR(255),
        CONSTRAINT unique_message_channel UNIQUE (message_id, channel)
    );
""")
conn.commit()

# === Load JSON files ===
raw_dir = "data/raw/telegram_messages"
media_root = "data/raw/media"
loaded_count = 0
skipped_files = 0

for root, _, files in os.walk(raw_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            channel_name = os.path.basename(root)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Handle both single message (dict) and list of messages
                messages = [data] if isinstance(data, dict) else data if isinstance(data, list) else []
                if not messages:
                    print(f"⚠️ Skipped {file_path} – not a valid JSON object or list")
                    skipped_files += 1
                    continue

                for msg in messages:
                    if not isinstance(msg, dict):
                        print(f"⚠️ Skipped non-dict message in {file_path}")
                        continue

                    msg_id = msg.get('id')
                    msg_text = msg.get('message') or msg.get('text')
                    msg_date = msg.get('date')

                    # Convert date
                    if msg_date:
                        try:
                            msg_date = datetime.fromisoformat(msg_date)
                        except Exception:
                            try:
                                msg_date = datetime.strptime(msg_date, "%Y-%m-%dT%H:%M:%S")
                            except Exception:
                                continue
                    else:
                        continue

                    # Get file_path from JSON, or guess it
                    file_path_field = msg.get('file_path')
                    if not file_path_field:
                        guessed_path = os.path.join(media_root, channel_name, f"{channel_name}_{msg_id}.jpg")
                        if os.path.exists(guessed_path):
                            file_path_field = guessed_path

                    # Insert into DB
                    cursor.execute("""
                        INSERT INTO raw.telegram_messages (message_id, date, text, channel, file_path)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT ON CONSTRAINT unique_message_channel DO NOTHING;
                    """, (msg_id, msg_date, msg_text, channel_name, file_path_field))
                    loaded_count += 1

            except Exception as e:
                print(f"⚠️ Skipped {file_path} due to error: {e}")
                skipped_files += 1

conn.commit()

# === Final Report ===
print(f"✅ Inserted {loaded_count} messages into raw.telegram_messages")
print(f"⚠️ Skipped {skipped_files} files")

# === Close connection ===
cursor.close()
conn.close()
