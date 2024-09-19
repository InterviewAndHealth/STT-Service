from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from utils import ClientConnection, init


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield


app = FastAPI(lifespan=lifespan)


@app.websocket("/stt")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    client = ClientConnection(websocket)
    await client.handle()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)
