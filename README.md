# Personal Paper Pilot (PPP)

A simple local-first document processing application that performs OCR, classifies documents, and extracts structured data.

## Features

- 📄 **OCR**: Extract text from images using Tesseract
- 🏷️ **Classification**: Automatic categorization (Jobcenter, Nebenkosten, Versicherung, Rechnung, Sonstiges)
- 💰 **Data Extraction**: Extract amounts and dates automatically
- 💾 **Local Storage**: All files and metadata stored locally
- 🌐 **Simple API**: RESTful API with web interface

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **OCR**: pytesseract, Tesseract OCR engine
- **Database**: SQLite
- **Frontend**: Minimal HTML interface

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-deu
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

## Usage

### Start the Server

```bash
cd backend
python main.py
```

The server will start at `http://127.0.0.1:8000`

### Upload Documents

1. Open `http://127.0.0.1:8000` in your browser
2. Drag and drop an image or click to upload
3. View extracted category, amounts, and dates

### API Endpoints

- `POST /upload` - Upload and process a document
- `GET /documents` - List all documents
- `GET /documents/{id}` - Get specific document
- `GET /category/{category}` - Get documents by category

## Testing with curl

```bash
# Upload a document
curl -X POST -F "file=@document.jpg" http://127.0.0.1:8000/upload

# List all documents
curl http://127.0.0.1:8000/documents

# Get documents by category
curl http://127.0.0.1:8000/category/Jobcenter
```

## Project Structure

```
backend/
├── main.py          # FastAPI application
├── ocr.py           # OCR processing
├── classifier.py    # Document classification
├── extractor.py     # Data extraction
├── storage.py       # File storage
└── database.py      # SQLite database
frontend/
└── index.html       # Upload interface
requirements.txt
```

## Classification Rules

Documents are classified by keyword detection:

| Keywords | Category |
|----------|----------|
| "jobcenter" | Jobcenter |
| "heizkosten", "nebenkosten" | Nebenkosten |
| "versicherung" | Versicherung |
| "rechnung" | Rechnung |
| (no match) | Sonstiges |

## File Storage

Files are stored in `data/documents/{category}/` with the naming format:
```
YYYY-MM-DD_originalname
```

## License

MIT
