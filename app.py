import streamlit as st
import pandas as pd
from PIL import Image
import io
import pdfplumber

st.title("📂 File Reader App")

# File uploader
uploaded_file = st.file_uploader(
    "Upload any file to read its content:",
    type=["txt", "csv", "xlsx", "xls", "jpg", "jpeg", "png", "pdf"]
)

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**File Type:** {file_type}")

    # Handle text files
    if file_type == "txt":
        content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content:", content, height=300)

    # Handle CSV files
    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

    # Handle Excel files
    elif file_type in ["xlsx", "xls"]:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)

    # Handle Image files
    elif file_type in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Handle PDF files
    elif file_type == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() or ""
            if all_text.strip():
                st.text_area("Extracted Text from PDF:", all_text, height=300)
            else:
                st.warning("No text found in this PDF (it may be scanned).")

else:
    st.info("👆 Upload a file to view its content.")
