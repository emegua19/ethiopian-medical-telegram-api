# Ethiopian Medical Telegram API

An end-to-end data product that scrapes, processes, analyzes, and exposes insights from Ethiopian medical product discussions on public Telegram channels.

All Tasks (Task 0–5) Completed  
Includes scraping, dbt modeling, YOLO image enrichment, FastAPI analytics, and Dagster orchestration.

---

## Project Overview

This project enables medical professionals, analysts, and policy-makers to:

- Scrape and collect messages and images from Ethiopian Telegram medical channels
- Structure and model the data using a star schema with dbt
- Apply YOLOv8 object detection on images
- Expose analytics via a FastAPI-based web API
- Orchestrate the entire pipeline with Dagster for scheduling and monitoring

---

## Tech Stack

| Area              | Tools/Tech              |
| ----------------- | ----------------------- |
| Scraping          | Telethon (Telegram API) |
| Data Storage      | JSON, PostgreSQL        |
| Data Modeling     | dbt                     |
| Image Enrichment  | YOLOv8 (Ultralytics)    |
| API Layer         | FastAPI, Uvicorn        |
| Orchestration     | Dagster                 |
| CI/CD             | GitHub Actions          |
| Containerization  | Docker                  |

---

## Project Structure

```plaintext
ethiopian-medical-telegram-api/
├── data/                     # Raw JSON, media, YOLO outputs
│   ├── raw/
│   └── yolo_outputs/
├── dbt/                      # dbt models (staging + marts)
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── schema.yml
├── src/
│   ├── api/                  # FastAPI app (main, crud, schemas, db)
│   ├── enrich.py             # YOLO detection code
│   ├── scrape.py             # Telegram scraper
│   ├── load.py               # Loader to PostgreSQL
├── dagster_pipeline/         # Dagster job, ops, schedule
├── tests/                    # Unit tests
├── docs/img/                 # Diagrams and visuals
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── setup_project.sh
└── README.md
````

---

## Features

### Task 1: Telegram Scraping

* Scrapes messages and image files from selected channels
* Stores messages in JSON and images in local folders

### Task 2: dbt Star Schema Modeling

* Builds `dim_channels`, `dim_dates`, `fct_messages`, and `fct_image_detections`
* Includes dbt tests and documentation

### Task 3: YOLOv8 Enrichment

* Applies object detection to images
* Extracts class name, confidence, and bounding boxes

### Task 4: FastAPI Analytical API

Available endpoints:

* `GET /api/search/messages?query=paracetamol`
* `GET /api/reports/top-products?limit=10`
* `GET /api/channels/{channel_name}/activity`

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### Task 5: Dagster Orchestration

* Ops:

  * `scrape_telegram_data`
  * `load_raw_to_postgres`
  * `run_dbt_transformations`
  * `run_yolo_enrichment`
* Pipeline executed from Dagster UI (`dagster dev`)
* Includes daily scheduling logic

---

## Testing

Run unit tests:

```bash
pytest tests/
```

Tested components:

* Scraping
* Data loading
* YOLO enrichment
* FastAPI routes

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/emegua19/ethiopian-medical-telegram-api.git
cd ethiopian-medical-telegram-api
```

### 2. Set Up `.env` File

```ini
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
DB_NAME=telegram_data
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Run the API

```bash
uvicorn src.api.main:app --reload
```

### 4. Run Dagster UI

```bash
dagster dev
```

Access the Dagster dashboard at [http://localhost:3000](http://localhost:3000)

---

## Screenshots and Diagrams

Located in `docs/img/`:

* `system_architecture.png`: Full pipeline architecture
* `pipeline_interim.png`: Initial working pipeline
* `scrape_log_sample.png`: Example logs
* `raw_data_table.png`: Preview of database messages

---

## Final Task Summary

| Task   | Description                           | Status    |
| ------ | ------------------------------------- | --------- |
| Task 0 | Setup, CI/CD, Docker, virtual env     | Completed |
| Task 1 | Scraping messages and images          | Completed |
| Task 2 | dbt modeling and validation           | Completed |
| Task 3 | YOLOv8 image detection                | Completed |
| Task 4 | FastAPI analytics                     | Completed |
| Task 5 | Dagster orchestration with scheduling | Completed |

---

## References

* [Telethon Documentation](https://docs.telethon.dev/)
* [dbt Documentation](https://docs.getdbt.com/)
* [YOLOv8 (Ultralytics)](https://docs.ultralytics.com/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Dagster](https://docs.dagster.io/)

---

## Author

**Yitbarek Geletaw**
10 Academy – Week 7 Final Submission
GitHub: https://github.com/emegua19/ethiopian-medical-telegram-api
