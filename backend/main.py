"""
Personal Paper Pilot - Main FastAPI Application
A simple document processing server with OCR, classification, and data extraction.
"""

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import tempfile
import os

from database import Database
from storage import Storage
from ocr import extract_text_from_image
from classifier import DocumentClassifier
from extractor import extract_all


# Initialize FastAPI app
app = FastAPI(
    title="Personal Paper Pilot",
    description="Local-first document processing with OCR and classification",
    version="1.0.0"
)

# Initialize services
db = Database()
storage = Storage()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend upload interface."""
    frontend_path = Path(__file__).parent.parent / "frontend" / "index.html"
    return FileResponse(frontend_path)


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document image.

    Performs:
    1. OCR to extract text
    2. Classification by keyword
    3. Data extraction (amounts, dates)
    4. File storage
    5. Database record creation

    Returns:
        JSON with category, amounts, and dates
    """
    # Validate file type - accept images only
    if not file.content_type:
        raise HTTPException(status_code=400, detail="Content-Type header is required")

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Please upload an image (JPG, PNG, etc.). PDFs are currently not supported."
        )

    # Save uploaded file to temporary location
    # Get file extension from original filename
    file_ext = ".jpg"
    if file.filename:
        if "." in file.filename:
            file_ext = "." + file.filename.rsplit(".", 1)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        # Step 1: Extract text using OCR
        try:
            text = extract_text_from_image(temp_path, lang="deu")
        except Exception as ocr_error:
            raise HTTPException(
                status_code=500,
                detail=f"OCR failed: {str(ocr_error)}. Make sure Tesseract OCR is installed."
            )

        # Step 2: Classify document
        category = DocumentClassifier.classify(text)

        # Step 3: Extract structured data
        extracted_data = extract_all(text)

        # Step 4: Store file
        relative_path = storage.save_file(temp_path, category, file.filename)

        # Step 5: Save to database
        db.save_document(
            filename=relative_path,
            category=category,
            text=text
        )

        # Return result
        return {
            "category": category,
            "amounts": extracted_data["amounts"],
            "dates": extracted_data["dates"]
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}\n\nTraceback: {traceback.format_exc()}"
        )

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@app.get("/documents")
async def list_documents():
    """Get all stored documents."""
    documents = db.get_all_documents()
    return {"documents": documents}


@app.get("/documents/{doc_id}")
async def get_document(doc_id: int):
    """Get a specific document by ID."""
    document = db.get_document(doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.get("/category/{category}")
async def get_by_category(category: str):
    """Get all documents of a specific category."""
    documents = db.get_documents_by_category(category)
    return {"documents": documents}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
