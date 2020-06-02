from fastapi import FastAPI

app = FastAPI(title="netmon-test-client")


@app.get("/client-api/ping")
async def ping():
    pass
