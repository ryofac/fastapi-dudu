from fastapi import FastAPI, status

app = FastAPI()


@app.get("/hello/", status_code=status.HTTP_200_OK)
async def hello_world():
    return {"hello": "world"}
