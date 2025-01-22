# PDF to DOCX Conversion Utilities

This repository contains Python scripts for converting PDF files to DOCX documents with different functionalities. The scripts leverage libraries such as `PyMuPDF`, `Pillow`, `python-docx`, and optionally `Tesseract` for OCR (Optical Character Recognition).

## Project Structure

```text
.
├── pdf2docx.py                 # PDF to DOCX conversion using graphical user interface
├── pdf2docx_centered_images.py # PDF to DOCX conversion with centered images
├── pdf2docx_with_ocr.py        # PDF to DOCX conversion with OCR for text extraction
├── poppler-wsl.docx            # Example output file
└── poppler-wsl.pdf             # Example input PDF file
```

## Features

1. **Basic Conversion (`pdf2docx.py`)**
   Converts PDF files to DOCX via a full-fledged graphical user interface.

2. **Centered Images Conversion (`pdf2docx_centered_images.py`)**
   Converts PDF files to DOCX with each page represented as a centered image in the Word document.

3. **OCR-Based Conversion (`pdf2docx_with_ocr.py`)**
   Uses Tesseract OCR to extract text from scanned or image-based PDFs and save it to a DOCX file.

## Requirements

- Python 3.7 or later
- The following Python libraries:
  - `fitz` (PyMuPDF)
  - `Pillow`
  - `python-docx`
  - `pytesseract` (for OCR functionality)

### Additional Tools for OCR

- **Tesseract OCR**:
  - Install Tesseract OCR from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
  - Ensure `tesseract` is added to your system's PATH.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Libraries**

   ```bash
   pip install pymupdf pillow python-docx pytesseract
   ```

4. **Set Up Tesseract (For OCR Functionality)**
   - Install Tesseract as described above.
   - Configure the path in `pdf2docx_with_ocr.py`:

     ```python
     pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract_executable'
     ```

5. **Run the Scripts**
   - **Conversion using Graphical User Interface**:

     ```bash
     python pdf2docx.py
     ```

   - **Centered Images Conversion**:

     ```bash
     python pdf2docx_centered_images.py
     ```

   - **OCR-Based Conversion**:

     ```bash
     python pdf2docx_with_ocr.py
     ```

## Examples

### Example Input and Output

- **Input PDF**: `poppler-wsl.pdf`
- **Generated DOCX**: `poppler-wsl.docx`

## Troubleshooting

1. **Tesseract Not Found**:
   - Ensure Tesseract is installed and added to your system's PATH.
   - Check if the correct path is configured in `pdf2docx_with_ocr.py`.

2. **Missing Dependencies**:
   - Reinstall the required libraries:

     ```bash
     pip install pymupdf pillow python-docx pytesseract
     ```

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

### Author

Developed with ❤️ to simplify PDF to DOCX conversions. For any queries, please reach out via GitHub issues.
