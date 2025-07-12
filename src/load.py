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
