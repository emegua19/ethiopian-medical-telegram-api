import os
import json
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from ultralytics import YOLO
from urllib.parse import quote_plus

# === Load environment variables ===
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))  # URL-encode special chars like '@'
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# === Connect to PostgreSQL ===
print("🔧 Connecting to:", f"{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

# === Query messages with images ===
query = """
    SELECT message_id, file_path, channel
    FROM raw.telegram_messages
    WHERE file_path ILIKE '%.jpg' OR file_path ILIKE '%.png'
"""

try:
    with engine.connect() as conn:
        messages = pd.read_sql(text(query), conn)
    print(f"✅ Loaded {len(messages)} image messages")
except Exception as e:
    print("❌ DB connection/query failed")
    raise e

# === Load YOLO model ===
model = YOLO("yolov8n.pt")

# === Process each image ===
results_list = []

for _, row in messages.iterrows():
    message_id = row["message_id"]
    image_path = row["file_path"]
    channel = row["channel"]

    if not os.path.exists(image_path):
        print(f"⚠️ File not found: {image_path}")
        continue

    try:
        results = model(image_path)

        # Create output directory
        output_dir = os.path.join("data/yolo_outputs", channel)
        os.makedirs(output_dir, exist_ok=True)


        # Plot and save annotated image
        annotated_img = results[0].plot()
        output_path = os.path.join(output_dir, f"{channel}_{message_id}.jpg")
        Image.fromarray(annotated_img).save(output_path)


        # Prepare detection list for this image
        image_detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                confidence = float(box.conf[0])

                detection = {
                    "message_id": message_id,
                    "channel": channel,
                    "class": class_name,
                    "confidence": confidence
                }

                results_list.append(detection)
                image_detections.append(detection)

        # Save per-image detections to JSON
        if image_detections:
            json_output_path = os.path.join(output_dir, f"{channel}_{message_id}_detections.json")
            with open(json_output_path, "w", encoding="utf-8") as f:
                json.dump(image_detections, f, indent=4)

    except Exception as e:
        print(f"❌ YOLO failed on {image_path}: {e}")

# === Save all detections to DB ===
if results_list:
    df_results = pd.DataFrame(results_list)
    try:
        df_results.to_sql("image_detections", engine, schema="raw", if_exists="replace", index=False)
        print(f"✅ Saved {len(df_results)} detections to raw.image_detections")
    except Exception as e:
        print("❌ Failed to save detections")
        raise e
else:
    print("⚠️ No detections to save")
