import asyncio
import random
from datetime import datetime
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Setup to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def events_source():
    """This is a generator that will yield a new event every second"""
    while True:
        event = random.sample(["datetime", "random"], 1)[0]
        if event == "datetime":
            yield f"event: datetime\ndata: {datetime.now()}\n\n"
        else:
            yield f"event: random\ndata: {random.random()}\n\n"
        await asyncio.sleep(1)

@app.get("/events")
async def events():
    """Return a StreamingResponse that streams events from the events_source()"""
    return StreamingResponse(
      events_source(),
      media_type="text/event-stream"
    )