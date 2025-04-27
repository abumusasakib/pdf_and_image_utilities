from pdf2image import convert_from_path
import os
from tqdm import tqdm
import zipfile

def pdf_to_jpg(pdf_file):
    # Create a directory to store the JPG files
    output_dir = os.path.splitext(pdf_file)[0] + "_images"
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_file, poppler_path=r'C:\Program Files\poppler-23.11.0\Library\bin')

    # Save each page as a JPG file
    print("Converting PDF to JPG:")
    for i, image in enumerate(tqdm(images, desc="Progress", unit="page")):
        image_path = os.path.join(output_dir, f"page_{i + 1}.jpg")
        image.save(image_path, "JPEG")

    print(f"\nConversion completed. {len(images)} pages converted to JPG.")

    # Archive images into a zip file
    zip_filename = os.path.splitext(pdf_file)[0] + "_images.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname=arcname)

    print(f"Images archived into {zip_filename}.")

if __name__ == "__main__":
    pdf_file = input("Enter the path to the PDF file: ")
    pdf_to_jpg(pdf_file)
