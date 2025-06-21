from markdown_pdf import MarkdownPdf, Section
import os

# === Configuration ===
INPUT_MARKDOWN_FILE = "facebook_pixel_flutter.md"
OUTPUT_PDF_FILE = "Facebook_App_Events_Integration_Guide.pdf"
DOCUMENT_TITLE = "Facebook App Events Integration Guide (Flutter)"
DOCUMENT_AUTHOR = "Your Name or Organization"

# === Load markdown content ===
with open(INPUT_MARKDOWN_FILE, "r", encoding="utf-8") as f:
    markdown_content = f.read()

# === Create PDF renderer with TOC and optimization ===
pdf = MarkdownPdf(toc_level=2, optimize=True)

# === Add main content as one section ===
pdf.add_section(
    Section(
        markdown_content,
        toc=True,
    ),
    user_css="""
            h1, h2, h3 { font-family: Arial; }
            pre, code { background-color: #f4f4f4; padding: 5px; border-radius: 3px; }
            a { color: #0645AD; text-decoration: underline; }
            body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.6; }
        """,
)

# === Add document metadata ===
pdf.meta["title"] = DOCUMENT_TITLE
pdf.meta["author"] = DOCUMENT_AUTHOR

# === Save to output file ===
pdf.save(OUTPUT_PDF_FILE)

print(f"✅ PDF successfully saved as: {OUTPUT_PDF_FILE}")
