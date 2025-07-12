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
    print("🚀 Dagster pipeline defined. Run with `dagster dev` UI.")

if __name__ == "__main__":
    main()
