# tests/test_db.py
import os
import sys
# ------------------------------------------------------------------ #
# Import project modules (add src to path)
# ------------------------------------------------------------------ #
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))

from src.api.database import SessionLocal
from sqlalchemy import text  # ✅ required import

def test_database_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # ✅ wrap SQL in text()
        db.close()
        assert True
    except Exception as e:
        print("❌ DB Error:", e)
        assert False, f"Failed to connect to the database: {e}"
