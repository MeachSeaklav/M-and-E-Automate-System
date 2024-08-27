import zipfile
import streamlit as st

def create_zip_file(word_filename, pdf_filename, zip_filename):
    try:
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(word_filename)
            zipf.write(pdf_filename)
        st.success(f"Zip file {zip_filename} created successfully.")
    except Exception as e:
        st.error(f"Failed to create zip file: {e}")
