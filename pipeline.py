from dagster import job, op, Out, In
import subprocess
import os
from datetime import datetime

@op
def scrape_telegram_data(context):
    # Execute src/scrape.py to scrape Telegram data
    result = subprocess.run(["python", "src/scrape.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraping failed: {result.stderr}")
    context.log.info("Telegram data scraped successfully")
    return {"timestamp": datetime.now().isoformat()}

@op
def load_raw_to_postgres(context, upstream_output):
    # Execute src/load.py to load raw data into PostgreSQL
    result = subprocess.run(["python", "src/load.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading failed: {result.stderr}")
    context.log.info("Raw data loaded to PostgreSQL")
    return {"loaded_at": upstream_output["timestamp"]}

@op
def run_dbt_transformations(context, upstream_output):
    # Run dbt transformations
    os.environ["DBT_PROFILES_DIR"] = "./dbt"
    result = subprocess.run(["dbt", "run", "--profiles-dir", "dbt"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    context.log.info("dbt transformations completed")
    return {"transformed_at": upstream_output["loaded_at"]}

@op
def run_yolo_enrichment(context, upstream_output):
    # Execute src/enrich.py for YOLO enrichment
    result = subprocess.run(["python", "src/enrich.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"YOLO enrichment failed: {result.stderr}")
    context.log.info("YOLO enrichment completed")
    return {"enriched_at": upstream_output["transformed_at"]}

@job
def telegram_pipeline():
    scrape_output = scrape_telegram_data()
    load_output = load_raw_to_postgres(scrape_output)
    transform_output = run_dbt_transformations(load_output)
    run_yolo_enrichment(transform_output)