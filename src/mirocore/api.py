from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def delivery_heaith_check():
    return {
        "satus": "ok",
        "message": "Hi, This is Miroc Core API."
    }