

##  `README.md` – Starter Template

```markdown
#  Ethiopian Medical Telegram API

An end-to-end data product that scrapes, processes, enriches, and exposes insights from Ethiopian medical product discussions on public Telegram channels.

---

##  Project Overview

This project is designed to help analysts and stakeholders gain insights from Telegram channels related to Ethiopian medical businesses. It includes:

- Automated scraping of Telegram messages and images
- Transformation of raw data into structured format using dbt
- Object detection on images using YOLOv8
- Analytical API endpoints powered by FastAPI
- Orchestrated data pipeline using Dagster

---

## 🛠️ Tech Stack

| Area                  | Tools/Tech               |
|-----------------------|--------------------------|
| Scraping              | Telethon (Telegram API)  |
| Data Lake & DB        | JSON, PostgreSQL         |
| Data Transformation   | dbt                      |
| Object Detection      | YOLOv8 (Ultralytics)     |
| API                   | FastAPI, Uvicorn         |
| Orchestration         | Dagster                  |
| Environment           | Docker, .env             |
| CI/CD                 | GitHub Actions           |

---

## 📁 Project Structure

```

ethiopian-medical-telegram-api/
├── data/                  # Raw data & YOLO outputs
├── dbt/                   # dbt project for transformation
├── src/                   # All source code
├── scripts/               # Bash scripts to run components
├── docker/                # Docker & Compose configs
├── .env                   # Secrets (excluded from Git)
├── requirements.txt       # Python dependencies
├── run\_pipeline.sh        # Optional runner script
└── .github/workflows/     # CI pipeline

````

---

##  Key Features

-  **Scrape** health-related messages & media from Telegram
-  **Clean & structure** data into a star schema using dbt
-  **Enrich** image data using YOLOv8 object detection
-  **Query insights** via API endpoints (e.g., top products, activity trends)
-  **Orchestrate** the whole pipeline using Dagster
-  **Dockerized** for consistent deployment

---

##  Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/emegua19/ethiopian-medical-telegram-api.git
cd ethiopian-medical-telegram-api
````

### 2. Create `.env` file

```ini
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
DB_NAME=telegram_data
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Build and Run via Docker

```bash
docker-compose up --build
```

---

## 🔌 API Endpoints (Example)

* `GET /api/reports/top-products?limit=10`
* `GET /api/channels/{channel_name}/activity`
* `GET /api/search/messages?query=paracetamol`

---

##  Tasks Overview

| Task   | Description                                      |
| ------ | ------------------------------------------------ |
| Task 0 | Environment setup (Docker, .env, GitHub Actions) |
| Task 1 | Telegram scraping and image collection           |
| Task 2 | Load and transform data using dbt (star schema)  |
| Task 3 | YOLOv8 object detection on images                |
| Task 4 | Analytical API with FastAPI                      |
| Task 5 | Full pipeline orchestration using Dagster        |

---

##  References

* [Telethon Docs](https://docs.telethon.dev/)
* [dbt Docs](https://docs.getdbt.com/)
* [Ultralytics YOLOv8](https://docs.ultralytics.com/)
* [FastAPI Docs](https://fastapi.tiangolo.com/)
* [Dagster](https://docs.dagster.io/)

---

## ✍️ Author

**Yitbarek Geletaw**
Project for 10 Academy – Week 7

---