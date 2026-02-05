from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Mammad! from FastAPI!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
