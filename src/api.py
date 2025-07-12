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
