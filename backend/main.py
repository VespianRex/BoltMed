from fastapi import FastAPI, File, UploadFile
from celery import Celery
import re

app = FastAPI()
celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task(name='perform_processing')
def perform_processing(file_content):
    # Placeholder OCR and text processing
    text = file_content.decode('utf-8')
    # Basic word extraction (replace with actual NLP later)
    words = re.findall(r'\b\w+\b', text.lower())
    # Example: Extract unique words longer than 5 characters
    extracted_terms = list(set(word for word in words if len(word) > 5))
    return extracted_terms

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
  contents = await file.read()
  print(f"Uploaded file: {file.filename} ({len(contents)} bytes)")
  task_result = perform_processing.delay(contents)
  extracted_terms = task_result.get()
  return {"extracted_terms": extracted_terms}
