# ReNew OCR Document Tracker

A Streamlit application that extracts data from procurement PDFs using OCR and AI, then maps the structured output to Excel tracker sheets matching ReNew's procurement workflow.

---

## Overview

This tool automates the manual process of reading procurement PDF documents and filling Excel tracker spreadsheets. It supports three procurement case types, each with a different document flow and tracker format.

### Supported Case Types

| Case | Description | Key Documents |
|------|-------------|---------------|
| **Case 1** | Import — EPC Clearance + Domestic Sale to SPV | Commercial Invoice, Packing List, Certificate of Origin, Bill of Lading, Bill of Entry, Duty Challan, E-way Bill, Tax Invoice, LR, GRN |
| **Case 2** | Import — HSS to SPV + Custom Clearance by SPV | Commercial Invoice, Packing List, Certificate of Origin, HSS Invoice, HSS Agreement, Bill of Lading, Bill of Entry, Duty Challan, E-way Bill, LR, GRN |
| **Case 3** | Domestic — Purchase by EPC + Sale to SPV | Tax Invoice (Supplier to EPC), Packing List, E-way Bill, Tax Invoice (EPC to SPV), LR, GRN |

---

## How It Works

1. **Upload PDF** — Select the case type and upload the procurement PDF.
2. **OCR Text Extraction** — Digital text is extracted via PyMuPDF. Scanned/image pages are processed in parallel using Tesseract OCR at 150 DPI.
3. **AI Data Extraction** — The combined text is sent to an LLM (via OpenRouter) with a case-specific prompt. The model returns structured JSON with all tracker fields.
4. **Map and Export** — The JSON is mapped to Excel column positions and written into the `Tracker_Format.xlsx` template. A filled Excel file is available for download.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| UI | Streamlit |
| PDF Text Extraction | PyMuPDF (fitz) |
| OCR (scanned pages) | Tesseract + Pillow |
| LLM Structuring | OpenRouter API (OpenAI-compatible) |
| Excel Output | openpyxl |
| Environment Config | python-dotenv |

---

## Project Structure

```
Renew_OCR/
├── app.py              # Streamlit UI and orchestration
├── config.py           # Case definitions, column mappings, model options
├── ocr_engine.py       # PyMuPDF + Tesseract text extraction (parallel)
├── extractor.py        # LLM-based data structuring via OpenRouter
├── mapper.py           # JSON fields to Excel column mapping
├── excel_writer.py     # Write data into tracker template
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed)
├── Tracker_Format.xlsx # Excel template with Case1/2/3 tracker sheets
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.10+
- Tesseract OCR installed on the system

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

### Installation

```bash
cd Renew_OCR
pip install -r requirements.txt
```

### API Key

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your key at [https://openrouter.ai/keys](https://openrouter.ai/keys).

---

## Usage

```bash
streamlit run app.py
```

1. The app opens in your browser.
2. Select a **Case Type** (1, 2, or 3) from the sidebar.
3. Optionally change the **LLM Model** in the sidebar.
4. Upload the procurement PDF.
5. Click **Process Document**.
6. Review the extracted data in the preview table.
7. Download the filled Excel tracker.

---

## Supported LLM Models

The following models are available via OpenRouter:

- Google Gemini 2.0 Flash (default)
- Google Gemini 2.5 Pro Preview
- Anthropic Claude Sonnet 4
- Meta Llama 4 Maverick
- DeepSeek Chat v3

---

## Configuration

### Column Mappings

Each case type maps semantic field names to specific Excel column numbers. These are defined in `config.py`:

- **Case 1**: 75 columns across 5 sections (Commercial Invoice, BoE, E-way Bill, Tax Invoice, Transportation)
- **Case 2**: 74 columns across 6 sections (adds HSS Invoice and HSS Agreement)
- **Case 3**: 65 columns across 4 sections (two Tax Invoices, E-way Bill, Transportation)

Data is written starting at **row 6** of the corresponding sheet in `Tracker_Format.xlsx`.

### OCR Settings

Configured in `ocr_engine.py`:

- **DPI**: 150 (configurable via `ocr_dpi` parameter)
- **Parallel workers**: 4 threads for Tesseract OCR
- **Text threshold**: Pages with fewer than 50 characters of digital text are sent to Tesseract
- **Blank detection**: Pages with no images are skipped entirely

---

## Notes

- Each PDF produces exactly **one row** in the tracker. Multiple values (e.g., several vehicle numbers) are comma-separated in a single cell.
- The `.env` file should not be committed to version control. Add it to `.gitignore`.
- The `Tracker_Format.xlsx` template must be present in the project root for Excel export to work.
