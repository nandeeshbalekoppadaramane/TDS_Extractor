# TDS Challan Extractor

A Streamlit app that pulls key fields out of TDS challan PDFs and combines them into one downloadable Excel. Upload one or many challans at once.

## What it extracts

For each challan PDF, the app reads the text layer (PyMuPDF) and applies tolerant regex patterns (several variants per field) to capture:

- Challan No / CIN
- Date of Deposit (or Tender Date)
- BSR Code
- Amount
- Breakup: Tax, Surcharge, Cess, Interest, Penalty, Fee under section 234E
- TAN
- Nature of Payment
- Assessment Year
- Financial Year

Fields that are not found come out blank rather than guessed - review the table before relying on it.

## Features

- **Multi-file upload** - drop any number of challan PDFs together.
- **Preview table** - extracted rows shown in the app before download.
- **One-click Excel** - all rows exported to a single `.xlsx` via openpyxl.

## Requirements

```bash
pip install -r requirements.txt
```

Dependencies: `streamlit`, `pymupdf`, `pandas`, `openpyxl`.

## Run

```bash
streamlit run TDS.py
```

1. Upload one or more TDS challan PDFs.
2. Check the extracted table.
3. Download the Excel.

## Notes

- Extraction depends on the challan's text layout; scanned-image PDFs without a text layer will not extract (no OCR).
- Everything runs locally; files are processed in memory and not uploaded anywhere.
- Private project.
