from fastapi import FastAPI, UploadFile, File, HTTPException
import pdfplumber
from transformers import pipeline

app = FastAPI()

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_chunks(chunks, max_length=130, min_length=30):
    summaries = []

    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        summaries.append(result[0]["summary_text"])

    return " ".join(summaries)

def chunk_text(text,max_chars = 2000):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""
    for p in paragraphs:
        if len(current_chunk)+len(p)<=max_chars:
            current_chunk += p + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = p + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

@app.post("/upload")
def process_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith("pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    try:
        file_text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    file_text += page_text + "\n"
        chunks = chunk_text(file_text)
        summary = summarize_chunks(chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text_length": len(file_text),
        "num_chunks": len(chunks),
        "summary": summary
    }
