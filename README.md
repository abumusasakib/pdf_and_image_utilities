# PDF and Image Utilities

This repository contains Python scripts for working with PDF files, DOCX documents, and image overlays. The scripts use libraries such as `PyMuPDF`, `Pillow`, `python-docx`, and `Tesseract` for OCR (Optical Character Recognition).

## Project Structure

```text
.
├── image_overlay_under_pdf.py  # Overlay an image under the content of PDF pages
├── pdf2jpg.py                  # Convert PDF pages to JPG images
├── pdf2docx.py                 # PDF to DOCX conversion using a graphical user interface
├── pdf2docx_centered_images.py # PDF to DOCX conversion with centered page images
├── pdf2docx_with_ocr.py        # PDF to DOCX conversion with OCR text extraction
├── poppler-wsl.docx            # Example output DOCX
├── poppler-wsl.pdf             # Example input PDF
├── README.md                   # This file
```

## Features

1. **Image Underlay for PDFs (`image_overlay_under_pdf.py`)**

   - Places a chosen image **under** the content of each page in a PDF.
   - Maintains the image's aspect ratio and centers it within the page.

2. **PDF to JPG Conversion (`pdf2jpg.py`)**

   - Converts each page of a PDF file into a separate JPG image.

3. **Conversion via GUI (`pdf2docx.py`)**

   - Converts PDF files to DOCX documents via a full-fledged graphical user interface (GUI).

4. **Centered Images Conversion (`pdf2docx_centered_images.py`)**

   - Converts PDF files to DOCX documents with each page represented as a centered image.

5. **OCR-Based Conversion (`pdf2docx_with_ocr.py`)**
   - Uses Tesseract OCR to extract text from scanned or image-based PDFs and saves it to a DOCX file.

---

## Quick Start Table

| Script                        | Purpose                                                        | How to Run                           |
| :---------------------------- | :------------------------------------------------------------- | :----------------------------------- |
| `image_overlay_under_pdf.py`  | Overlay an image **under** PDF pages, maintaining aspect ratio | `python image_overlay_under_pdf.py`  |
| `pdf2jpg.py`                  | Convert PDF pages to separate **JPG images**                   | `python pdf2jpg.py`                  |
| `pdf2docx.py`                 | Convert PDF to **DOCX via GUI**                                | `python pdf2docx.py`                 |
| `pdf2docx_centered_images.py` | Convert PDF pages to **centered images** inside DOCX           | `python pdf2docx_centered_images.py` |
| `pdf2docx_with_ocr.py`        | Extract **text using OCR** from PDFs into DOCX                 | `python pdf2docx_with_ocr.py`        |

---

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

   - Install Tesseract.
   - Configure the Tesseract executable path in scripts like `pdf2docx_with_ocr.py` and `pdf2docx.py`:

     ```python
     pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract_executable'
     ```

## Usage

- **Overlay Image Under PDF Content**:

  ```bash
  python image_overlay_under_pdf.py
  ```

- **Convert PDF to JPG Images**:

  ```bash
  python pdf2jpg.py
  ```

- **PDF to DOCX (GUI-Based Conversion)**:

  ```bash
  python pdf2docx.py
  ```

- **PDF to DOCX with Centered Images**:

  ```bash
  python pdf2docx_centered_images.py
  ```

- **PDF to DOCX with OCR Text Extraction**:

  ```bash
  python pdf2docx_with_ocr.py
  ```

## Examples

### Example Input and Output

- **Input PDF**: `poppler-wsl.pdf`
- **Generated DOCX**: `poppler-wsl.docx`

You can find examples in this repository demonstrating PDF input and the corresponding DOCX output.

## Troubleshooting

1. **Tesseract Not Found**:

   - Ensure Tesseract is installed and available in your system PATH.
   - Double-check the `tesseract_cmd` path configuration.

2. **Missing Dependencies**:

   - Reinstall the required libraries:

     ```bash
     pip install pymupdf pillow python-docx pytesseract
     ```

3. **Images Not Visible Under PDF Content**:
   - Some PDFs draw a solid white background layer which might cover the underlaid image. Open an issue if you need help handling this.

## Contributions

Contributions are welcome!
Feel free to open issues, suggest improvements, or submit pull requests.

---

### Author

Developed with ❤️ to simplify PDF and document-related workflows.
For any queries, please reach out via GitHub Issues.
