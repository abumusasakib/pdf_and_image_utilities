# PDF and Image Utilities

This repository contains Python scripts for working with PDF files, DOCX documents, and image overlays. The scripts use libraries such as `PyMuPDF`, `Pillow`, `python-docx`, `markdown-pdf` and `Tesseract` for OCR (Optical Character Recognition).

## Project Structure

```text
.
├── image_overlay_under_pdf.py  # Overlay an image under the content of PDF pages
├── pdf2jpg.py                  # Convert PDF pages to JPG images
├── md2pdf.py                   # Convert Markdown to PDF
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

6. **Markdown to PDF Conversion (`md2pdf.py`)**
   - Converts a Markdown document into a high-quality PDF with a table of contents, custom CSS styling, and proper metadata using the `markdown-pdf` library.

   This utility (`md2pdf.py`) allows you to:
   - Render structured Markdown (including headings, lists, links, code blocks, and tables) into a styled PDF.
   - Embed custom CSS for layout and typography control.
   - Automatically include a **Table of Contents (TOC)** as bookmarks.
   - Define document metadata (title, author).
   - Ideal for generating user manuals or documentation PDFs from Markdown source files.

   **Quick Start:**
   1. Install the library:

      ```bash
      pip install markdown-pdf
      ```

   2. Run the script:

      ```bash
      python md2pdf.py
      ```

---

## Quick Start Table

| Script                         | Description                                                    | How to Run                            |
|-------------------------------|----------------------------------------------------------------|----------------------------------------|
| `image_overlay_under_pdf.py`  | Overlay an image **beneath** PDF page content (preserving aspect ratio) | `python image_overlay_under_pdf.py`   |
| `pdf2jpg.py`                  | Convert each PDF page into a high-resolution **JPG image**     | `python pdf2jpg.py`                   |
| `pdf2docx.py`                 | Convert PDF to **editable DOCX** using a graphical interface   | `python pdf2docx.py`                  |
| `pdf2docx_centered_images.py` | Convert PDF pages into **centered images** inside a DOCX file  | `python pdf2docx_centered_images.py`  |
| `pdf2docx_with_ocr.py`        | Convert scanned PDFs to DOCX with **OCR-extracted text**       | `python pdf2docx_with_ocr.py`         |
| `md2pdf.py`                   | Convert Markdown files into **styled, high-quality PDFs** with TOC | `python md2pdf.py`                    |

---

## Requirements

- Python 3.7 or later
- The following Python libraries:
  - `fitz` (PyMuPDF)
  - `Pillow`
  - `python-docx`
  - `pytesseract` (for OCR functionality)
  - `markdown-pdf` (for Markdown conversion)

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
   pip install pymupdf pillow python-docx pytesseract markdown-pdf
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

- **Convert Markdown to PDF**:

  ```bash
  python md2pdf.py
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

You can find examples in this repository input and output of the scripts.

## Troubleshooting

1. **Tesseract Not Found**:

   - Ensure Tesseract is installed and available in your system PATH.
   - Double-check the `tesseract_cmd` path configuration.

2. **Missing Dependencies**:

   - Reinstall the required libraries:

     ```bash
     pip install pymupdf pillow python-docx pytesseract markdown-pdf
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
