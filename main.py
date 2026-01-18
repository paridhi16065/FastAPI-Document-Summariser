from fastapi import FastAPI, UploadFile, File, HTTPException
import pdfplumber

app = FastAPI()

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "text_length": len(file_text)
    }
