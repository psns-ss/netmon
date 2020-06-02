from fastapi import FastAPI

app = FastAPI(title="netmon-test-client")


@app.get("/client-api/ping")
async def ping():
    pass


@app.get("/client-api/interfaces")
async def get_interfaces():
    return [{"Name": "lo0"}]


@app.get("/client-api/active-processes")
async def get_active_processes():
    return [
        {
            "Name": "skype",
            "Hash": "0959002856fdcbb9616b3bc2961a952b49965b2cd6cb167f9fbc689a5aa8fb64",
        },
        {
            "Name": "word",
            "Hash": "ad46fa2b41cba0f8a6cf0f1fb32a388c257f14e6a295109fa793daea96270ab8",
        },
    ]
