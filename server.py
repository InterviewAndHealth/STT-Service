from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils import ClientConnection, init


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the STT service"}


@app.websocket("/stt")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    client = ClientConnection(websocket)
    await client.handle()


if __name__ == "__main__":
    import uvicorn
    import os

    HOST = os.getenv("HOST", "localhost")
    PORT = os.getenv("PORT", 8000)

    uvicorn.run(app, host=HOST, port=PORT)
