from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Hello, MBA Portfolio Analyzer is alive!"}
