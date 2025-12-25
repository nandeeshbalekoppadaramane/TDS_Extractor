import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="TDS Challan Extractor", page_icon="📄", layout="centered")

# ======== Title Section ========
st.title("📄 TDS Challan PDF Extractor")
st.write("Easily extract data from multiple TDS Challan PDFs and download the result as Excel.")

# ======== File Upload ========
uploaded_files = st.file_uploader("Upload one or more TDS Challan PDF files", type=["pdf"], accept_multiple_files=True)

# ======== Regex Patterns ========
patterns = {
    "Challan No": [
        r"Challan\s*No\s*:\s*(\d+)",
        r"CIN\s*:\s*(\d+[A-Z]+)",
        r"Challan\s*Number\s*:\s*(\d+)"
    ],
    "Date of Deposit": [
        r"Date\s*of\s*Deposit\s*:\s*(\d{1,2}-[A-Za-z]{3}-\d{4})",
        r"Date\s*of\s*Deposit\s*:\s*(\d{1,2}/\d{1,2}/\d{4})",
        r"Tender\s*Date\s*:\s*(\d{1,2}/\d{1,2}/\d{4})"
    ],
    "BSR Code": [
        r"BSR\s*code\s*:\s*(\d{7})",
        r"BSR\s*Code\s*:\s*(\d{7})",
        r"BSR\s*:\s*(\d{7})"
    ],
    "Amount": [
        r"Amount\s*\(in\s*Rs\.\)\s*:\s*₹\s*([\d,]+)",
        r"Total\s*\([A-Z+]+\)\s*₹\s*([\d,]+)",
        r"Amount\s*:\s*₹\s*([\d,]+)"
    ],
    "Tax": [
        r"A\s*Tax\s*₹\s*([\d,]+)",
        r"Tax\s*₹\s*([\d,]+)",
        r"Income\s*Tax\s*₹\s*([\d,]+)"
    ],
    "Surcharge": [
        r"B\s*Surcharge\s*₹\s*([\d,]+)",
        r"Surcharge\s*₹\s*([\d,]+)"
    ],
    "Cess": [
        r"C\s*Cess\s*₹\s*([\d,]+)",
        r"Cess\s*₹\s*([\d,]+)",
        r"Education\s*Cess\s*₹\s*([\d,]+)"
    ],
    "Interest": [
        r"D\s*Interest\s*₹\s*([\d,]+)",
        r"Interest\s*₹\s*([\d,]+)"
    ],
    "Penalty": [
        r"E\s*Penalty\s*₹\s*([\d,]+)",
        r"Penalty\s*₹\s*([\d,]+)"
    ],
    "Fee under 234E": [
        r"F\s*Fee\s*under\s*section\s*234E\s*₹\s*([\d,]+)",
        r"Fee\s*under\s*section\s*234E\s*₹\s*([\d,]+)",
        r"234E\s*₹\s*([\d,]+)"
    ],
    "TAN": [
        r"TAN\s*:\s*([A-Z0-9]+)",
        r"TAN\s*Number\s*:\s*([A-Z0-9]+)"
    ],
    "Nature of Payment": [
        r"Nature\s*of\s*Payment\s*:\s*(\d+[A-Z]*)",
        r"Section\s*:\s*(\d+[A-Z]*)"
    ],
    "Assessment Year": [
        r"Assessment\s*Year\s*:\s*(\d{4}-\d{2})",
        r"AY\s*:\s*(\d{4}-\d{2})"
    ],
    "Financial Year": [
        r"Financial\s*Year\s*:\s*(\d{4}-\d{2})",
        r"FY\s*:\s*(\d{4}-\d{2})"
    ]
}

def extract_field(text, field_patterns):
    for pattern in field_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            return "" if value == "0" else value
    return ""

def clean_amount(amount_str):
    if amount_str:
        return re.sub(r'[,\s]', '', amount_str)
    return ""

def process_pdfs(files):
    results = []
    for file in files:
        try:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            text = re.sub(r"\s+", " ", text).strip()
            extracted = {'File': file.name}

            for field, field_patterns in patterns.items():
                value = extract_field(text, field_patterns)
                if field in ["Amount", "Tax", "Surcharge", "Cess", "Interest", "Penalty", "Fee under 234E"]:
                    value = clean_amount(value)
                extracted[field] = value

            results.append(extracted)
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
            error_row = {'File': file.name, 'Error': str(e)}
            results.append(error_row)
    return results

# ======== Process Button ========
if st.button("🔍 Extract Data"):
    if not uploaded_files:
        st.warning("Please upload at least one PDF file.")
    else:
        with st.spinner("Processing PDFs... Please wait..."):
            results = process_pdfs(uploaded_files)
            if results:
                df = pd.DataFrame(results)
                st.success("✅ Extraction complete!")

                st.dataframe(df)

                output = BytesIO()
                df.to_excel(output, index=False)
                st.download_button(
                    label="📥 Download Excel File",
                    data=output.getvalue(),
                    file_name="TDS_Challan_Extracted_Data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("No data extracted from the uploaded files.")

# ======== Creator Section ========
st.markdown("---")
st.subheader("👨‍💻 Creator")
st.markdown("""
**Created by [Nandeesh Balekoppadaramane](https://www.linkedin.com/in/nandeesh-balekoppadaramane)**  
Passionate about **automation, self-development, and innovation**.  
This app was built to simplify TDS challan data extraction for professionals and businesses.
""")
