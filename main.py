import json
import traceback

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

from extractors import extract_content
from generator import stream_repurposed_content

app = FastAPI(title="Content Repurposer")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(
    input_type: str = Form(...),
    platform: str = Form(...),
    content: str = Form(...),
):
    async def event_stream():
        try:
            extracted = extract_content(input_type, content)
            async for chunk in stream_repurposed_content(platform, extracted):
                yield {"event": "token", "data": json.dumps({"text": chunk})}
            yield {"event": "done", "data": "{}"}
        except Exception as e:
            traceback.print_exc()
            yield {"event": "error", "data": json.dumps({"message": str(e)})}

    return EventSourceResponse(event_stream())
