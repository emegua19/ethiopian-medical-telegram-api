#!/bin/bash

# Set your custom project root folder
PROJECT_NAME="ethiopian-medical-telegram-api"

echo "📁 Creating project structure..."
mkdir -p $PROJECT_NAME/{data/raw,data/yolo_outputs,dbt/models/{staging,marts},src,docker,scripts,.github/workflows}

# Basic files
touch $PROJECT_NAME/{.env,.gitignore,README.md,requirements.txt,run_pipeline.sh}

# -----------------------------
# Python Scripts with main()
# -----------------------------

# scrape.py
cat <<EOF > $PROJECT_NAME/src/scrape.py
import os
from dotenv import load_dotenv

def scrape_telegram_channels():
    print("🔍 Scraping Telegram channels...")
    # TODO: Implement scraping logic with Telethon
    pass

def main():
    load_dotenv()
    scrape_telegram_channels()

if __name__ == "__main__":
    main()
EOF

# load.py
cat <<EOF > $PROJECT_NAME/src/load.py
import os
from dotenv import load_dotenv

def load_raw_data_to_postgres():
    print("📥 Loading raw JSON data into PostgreSQL...")
    # TODO: Parse JSON files and insert into raw schema
    pass

def main():
    load_dotenv()
    load_raw_data_to_postgres()

if __name__ == "__main__":
    main()
EOF

# enrich.py
cat <<EOF > $PROJECT_NAME/src/enrich.py
import os
from dotenv import load_dotenv

def run_yolo_enrichment():
    print("🧠 Running YOLOv8 detection on images...")
    # TODO: Load images, run YOLOv8, save detection results
    pass

def main():
    load_dotenv()
    run_yolo_enrichment()

if __name__ == "__main__":
    main()
EOF

# api.py
cat <<EOF > $PROJECT_NAME/src/api.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ethiopian Medical Telegram API is running!"}

@app.get("/api/reports/top-products")
def get_top_products(limit: int = 10):
    # TODO: Query DB and return top products
    return {"top_products": []}

def main():
    import uvicorn
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
EOF

# dagster_pipeline.py
cat <<EOF > $PROJECT_NAME/src/dagster_pipeline.py
from dagster import job, op

@op
def scrape_op():
    from src.scrape import scrape_telegram_channels
    scrape_telegram_channels()

@op
def load_op():
    from src.load import load_raw_data_to_postgres
    load_raw_data_to_postgres()

@op
def enrich_op():
    from src.enrich import run_yolo_enrichment
    run_yolo_enrichment()

@job
def telegram_pipeline():
    scrape_op()
    load_op()
    enrich_op()

def main():
    print("🚀 Dagster pipeline defined. Run with \`dagster dev\` UI.")

if __name__ == "__main__":
    main()
EOF

# -----------------------------
# Shell Scripts
# -----------------------------
cat <<EOF > $PROJECT_NAME/scripts/scrape.sh
#!/bin/bash
python src/scrape.py
EOF

cat <<EOF > $PROJECT_NAME/scripts/load.sh
#!/bin/bash
python src/load.py
EOF

cat <<EOF > $PROJECT_NAME/scripts/enrich.sh
#!/bin/bash
python src/enrich.py
EOF

cat <<EOF > $PROJECT_NAME/scripts/api.sh
#!/bin/bash
uvicorn src.api:app --reload --port 8000
EOF

cat <<EOF > $PROJECT_NAME/scripts/pipeline.sh
#!/bin/bash
bash scripts/scrape.sh
bash scripts/load.sh
bash scripts/enrich.sh
EOF

chmod +x $PROJECT_NAME/scripts/*.sh

# -----------------------------
# Docker and CI Config
# -----------------------------
cat <<EOF > $PROJECT_NAME/docker/Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

cat <<EOF > $PROJECT_NAME/docker/docker-compose.yml
version: "3.8"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: \${DB_NAME}
      POSTGRES_USER: \${DB_USER}
      POSTGRES_PASSWORD: \${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - TELEGRAM_API_ID=\${TELEGRAM_API_ID}
      - TELEGRAM_API_HASH=\${TELEGRAM_API_HASH}
      - DB_USER=\${DB_USER}
      - DB_PASSWORD=\${DB_PASSWORD}
      - DB_NAME=\${DB_NAME}

volumes:
  pg_data:
EOF

cat <<EOF > $PROJECT_NAME/.github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run script checks
      run: |
        echo "✅ Scripts ready. Add real tests here."
EOF

# -----------------------------
echo "✅ Project '$PROJECT_NAME' initialized successfully!"
