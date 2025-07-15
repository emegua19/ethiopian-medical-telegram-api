import os
import json
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'telegram_db')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD')

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cursor = conn.cursor()

# Drop table if it exists to ensure constraint is applied
cursor.execute("DROP TABLE IF EXISTS raw.telegram_messages;")
conn.commit()

# Create raw schema if it doesn't exist
cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
conn.commit()

# Create raw.telegram_messages table with unique constraint
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

# Load JSON files from data lake
raw_dir = "data/raw/telegram_messages"
for root, _, files in os.walk(raw_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S%z')
                cursor.execute("""
                    INSERT INTO raw.telegram_messages (message_id, date, text, channel, file_path)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT unique_message_channel DO NOTHING;
                """, (data['id'], date, data['text'], data['channel'], file_path))
conn.commit()

# Close connection
cursor.close()
conn.close()