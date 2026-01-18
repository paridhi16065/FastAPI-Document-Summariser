# FastAPI-Document-Summariser
Document processing and summarising API
A FastAPI-based service that ingests PDF documents, extracts text, chunks long inputs, and applies transformer-based summarisation with explicit validation and error handling.

## Overview

This service:
- Accepts PDF uploads via a REST API
- Validates file types at the API boundary
- Extracts text from PDFs
- Chunks long documents to respect model limits
- Applies a pretrained transformer model to generate summaries
- Returns structured JSON responses

## Architecture

Client → FastAPI → PDF Text Extraction → Chunking → Summarisation Model → JSON Response
The model is loaded once at startup to avoid load at request time

## Design Decisions

- **FastAPI** was chosen for explicit request/response schemas and automatic API documentation.
- **MIME-type validation** is performed before processing to fail fast on unsupported inputs.
- **Paragraph-based chunking** is used to preserve semantic coherence while staying within transformer limits.
- **Synchronous processing** was chosen for simplicity since summarisation is CPU-bound.

## Limitations and Bias Considerations

- Image-based (scanned) PDFs are not supported.
- The summarisation model may hallucinate demographic attributes (e.g., gendered pronouns) not present in the source text.
- This behavior reflects known biases in pretrained language models trained on web-scale data.
- In a production system, mitigation could include constrained decoding, post-processing, or human review.

## Running the Service

pip install -r requirements.txt  
uvicorn main:app --reload

The API documentation is available at http://127.0.0.1:8000/docs

## Running with Docker

The service can also be run in a Docker container for a reproducible environment.

docker build -t doc-summarizer .
docker run -p 8000:8000 doc-summarizer