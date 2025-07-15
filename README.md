#  Ethiopian Medical Telegram API

An end-to-end data product that scrapes, processes, and structures insights from Ethiopian medical product discussions on public Telegram channels. This version reflects progress up to Task 2 (Interim Report).

---

##  Project Overview

This project helps analysts monitor and understand Ethiopian medical market activity by:

* Scraping public Telegram messages and images
* Structuring data using a star schema via dbt
* Preparing data for future enrichment (YOLOv8) and API delivery (FastAPI)

---

## 🛠️ Tech Stack

| Area              | Tools/Tech              |
| ----------------- | ----------------------- |
| Scraping          | Telethon (Telegram API) |
| Data Storage      | JSON (Data Lake)        |
| Database          | PostgreSQL              |
| Transformation    | dbt                     |
| Future Enrichment | YOLOv8 (Ultralytics)    |
| API (Planned)     | FastAPI, Uvicorn        |
| Orchestration     | Dagster (Planned)       |
| Dev Environment   | Docker, .env            |
| CI/CD             | GitHub Actions          |

---

## 📁 Project Structure

```plaintext
ethiopian-medical-telegram-api/
├── data/                     # Raw JSON + media, YOLO outputs
│   ├── raw/
│   └── yolo_outputs/
├── dbt/                      # dbt project for transformation
├── docker/                   # Docker and docker-compose setup
├── report/                   # LaTeX report and visuals
├── scripts/                  # Bash runner scripts
│   ├── run_scrape.py
│   └── run_pipeline.sh
├── src/                      # All core scripts (scrape, load, etc.)
├── .env                      # Credentials (excluded from Git)
├── .github/workflows/        # CI pipelines
├── requirements.txt          # Python dependencies
├── setup_project.sh          # Local setup script
└── README.md                 # Project overview (this file)
```

---

##  Key Features So Far

*  Scrapes public Telegram messages & images from selected medical channels
*  Stores them as JSON in a structured date-partitioned Data Lake
*  Loads messages into a PostgreSQL `raw.telegram_messages` table
*  Transforms data using dbt into a star schema:

  * `dim_channels`, `dim_dates`, `fct_messages`
* ✅ Validates data using dbt tests and generates documentation

---

##  Quick Start (Local Environment)

### 1. Clone the repository

```bash
git clone https://github.com/emegua19/ethiopian-medical-telegram-api.git
cd ethiopian-medical-telegram-api
```

### 2. Create `.env` file

```ini
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
DB_NAME=telegram_data
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Activate virtual environment (if Docker fails)

```bash
chmod +x setup_project.sh
./setup_project.sh
```

---

## 🔌 Planned API Endpoints (For Future Tasks)

* `GET /api/reports/top-products?limit=10`
* `GET /api/channels/{channel_name}/activity`
* `GET /api/search/messages?query=paracetamol`

---

##  Tasks Overview

| Task   | Description                                  | Status      |
| ------ | -------------------------------------------- | ----------- |
| Task 0 | Setup (Docker, venv, CI, secrets)            | ✅ Completed |
| Task 1 | Telegram message scraping + media collection | ✅ Completed |
| Task 2 | Load & transform with dbt (star schema)      | ✅ Completed |
| Task 3 | YOLOv8 object detection                      | 🔜 Upcoming |
| Task 4 | Analytical API with FastAPI                  | 🔜 Upcoming |
| Task 5 | Dagster orchestration of full pipeline       | 🔜 Upcoming |

---

##  Screenshots (See `/docs/img/`)

* `system_architecture.png`: Overview of all components
* `pipeline_interim.png`: Current working pipeline
* `scrape_log_sample.png`: Sample scraping logs
* `raw_data_table.png`: PostgreSQL message table preview

---

##  References

* [Telethon Docs](https://docs.telethon.dev/)
* [dbt Documentation](https://docs.getdbt.com/)
* [YOLOv8](https://docs.ultralytics.com/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Dagster](https://docs.dagster.io/)

---

## ✍️ Author

**Yitbarek Geletaw**
10 Academy — Week 7 Interim Report
