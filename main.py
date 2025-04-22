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

@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "base64_data": "", "encoding": "", "result": None, "error": None})


@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, base64_data: str = Form(...), encoding: str = Form('auto')):
    try:
        buffer_data = base64.b64decode(base64_data)
        detected_encoding = detect_encoding(buffer_data) if encoding == 'auto' else encoding
        text_content = buffer_data.decode(detected_encoding)
        return templates.TemplateResponse("form.html", {"request": request, "base64_data": base64_data, "encoding": encoding, "result": result, "error": error})
    except Exception as e:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "result": None,
            "encoding": None,
            "error": str(e)
        })
