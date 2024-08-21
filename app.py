from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Hello world!"}

@app.get("/items/{item_id}")
def return_item(item_id: int):
    return {"item": item_id}