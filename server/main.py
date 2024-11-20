import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/contents/{content_id}")
async def read_content(content_id: int):
    data = bytearray(100 * 1024 * 1024)
    # Convert bytearray to a BytesIO stream
    stream = io.BytesIO(data)

    # Return the stream as a response
    return StreamingResponse(stream, media_type="application/octet-stream")
