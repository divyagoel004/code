from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import base64
import chardet

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def detect_encoding(binary_data):
    detection = chardet.detect(binary_data)
    return detection['encoding'] if detection['encoding'] else 'utf-8'

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "result": None, "error": None})

@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, base64_data: str = Form(...), encoding: str = Form("auto")):
    try:
        buffer_data = base64.b64decode(base64_data)
    except Exception as e:
        return templates.TemplateResponse("form.html", {"request": request, "result": None, "error": f"Invalid base64 data: {str(e)}"})

    detected_encoding = detect_encoding(buffer_data) if encoding == 'auto' else encoding

    try:
        text_content = buffer_data.decode(detected_encoding)
    except Exception as e:
        return templates.TemplateResponse("form.html", {"request": request, "result": None, "error": f"Decoding error: {str(e)}"})

    return templates.TemplateResponse("form.html", {"request": request, "result": text_content, "error": None})
