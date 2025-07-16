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

# === Create schema and table ===
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cursor.execute("DROP TABLE IF EXISTS raw.telegram_messages;")
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

# === Load individual JSON message files ===
raw_dir = "data/raw/telegram_messages"
loaded_count = 0

for root, _, files in os.walk(raw_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            channel_name = os.path.basename(root)  # folder = channel
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    msg = json.load(f)  # now msg is ONE dict
                    msg_id = msg.get('id')
                    msg_text = msg.get('message') or msg.get('text')
                    msg_date = msg.get('date')
                    if msg_date:
                        msg_date = datetime.fromisoformat(msg_date)
                    else:
                        continue  # skip if no date

                    cursor.execute("""
                        INSERT INTO raw.telegram_messages (message_id, date, text, channel, file_path)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT ON CONSTRAINT unique_message_channel DO NOTHING;
                    """, (msg_id, msg_date, msg_text, channel_name, file_path))
                    loaded_count += 1
                except Exception as e:
                    print(f"⚠️ Skipped {file_path} due to error: {e}")

conn.commit()
print(f" Inserted {loaded_count} messages into raw.telegram_messages")

# === Close connection ===
cursor.close()
conn.close()
