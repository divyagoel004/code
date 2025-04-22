from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import chardet

app = FastAPI()

class BufferInput(BaseModel):
    base64_data: str
    encoding: str = 'auto'

def detect_encoding(binary_data):
    detection = chardet.detect(binary_data)
    return detection['encoding'] if detection['encoding'] else 'utf-8'

@app.post("/convert-buffer/")
async def convert_buffer(input_data: BufferInput):
    try:
        buffer_data = base64.b64decode(input_data.base64_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")

    encoding = detect_encoding(buffer_data) if input_data.encoding == 'auto' else input_data.encoding

    try:
        text_content = buffer_data.decode(encoding)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decoding error: {str(e)}")

    return {"text": text_content, "encoding": encoding}
