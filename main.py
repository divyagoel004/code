from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import chardet

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def detect_encoding(binary_data):
    detection = chardet.detect(binary_data)
    return detection['encoding'] if detection['encoding'] else 'utf-8'

def hex_to_bytes(hex_string):
    # Remove spaces from the hex string
    hex_string = hex_string.replace(" ", "")
    # Convert hex string to bytes
    return bytes.fromhex(hex_string)

@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "hex_data": "", "encoding": "", "result": None, "error": None})

@app.post("/", response_class=HTMLResponse)
async def handle_form(request: Request, hex_data: str = Form(...), encoding: str = Form('auto')):
    try:
        # Convert hex string to bytes
        buffer_data = hex_to_bytes(hex_data)
        # Detect or use provided encoding
        detected_encoding = detect_encoding(buffer_data) if encoding == 'auto' else encoding
        # Decode bytes to text
        text_content = buffer_data.decode(detected_encoding)
        return templates.TemplateResponse("form.html", {
            "request": request, 
            "hex_data": hex_data, 
            "encoding": detected_encoding, 
            "result": text_content, 
            "error": None
        })
    except Exception as e:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "hex_data": hex_data,
            "encoding": encoding,
            "result": None,
            "error": str(e)
        })
