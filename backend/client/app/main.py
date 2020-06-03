from fastapi import FastAPI

app = FastAPI(title="netmon-test-client")


@app.get("/client-api/ping")
async def ping():
    pass


@app.get("/client-api/interfaces")
async def get_interfaces():
    return [
        {
            "InterfaceDescription": "Qualcomm Atheros",
            "IPv4Address": "192.168.0.12",
            "IPv4DefaultGateway": "192.168.0.1",
            "DNSServer": "192.168.0.1",
        },
        {
            "InterfaceDescription": "Qualcomm",
            "IPv4Address": "192.168.0.17",
            "IPv4DefaultGateway": "192.168.0.1",
            "DNSServer": "192.168.0.1",
        },
    ]


@app.get("/client-api/active-processes")
async def get_active_processes():
    return [
        {
            "Name": "svhost",
            "Id": 4786777848,
            "Path": "C:\Windows\system32\svhost.exe",
            "Hash": "0959002856fdcbb9fsf616b3bc2961a2b49962cdcb1fdsfs67f9fbc689a5aa8fb64",
        },
        {
            "Name": "sfile",
            "Id": 478600,
            "Path": "C:\Windows\system32\sfile.exe",
            "Hash": "0959002856fdcbb9616b3bc2961a952b4995b2d6cb167f9fdsffbc689a5aa8fb64f",
        },
    ]
