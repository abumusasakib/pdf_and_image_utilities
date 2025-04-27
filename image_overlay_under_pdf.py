from io import BytesIO
from PIL import Image
import fitz  # PyMuPDF
from tkinter import Tk, filedialog, messagebox


def overlay_image_under_pdf_content():
    root = Tk()
    root.withdraw()  # Hide the root window

    try:
        # Select the PDF file
        pdf_file = filedialog.askopenfilename(
            title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")]
        )
        if not pdf_file:
            messagebox.showinfo(
                "No File Selected", "You must select a PDF file to continue."
            )
            return

        # Select the image file
        image_file = filedialog.askopenfilename(
            title="Select an Image file",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")],
        )
        if not image_file:
            messagebox.showinfo(
                "No Image Selected", "You must select an image to continue."
            )
            return

        # Select the output PDF save location
        output_pdf = filedialog.asksaveasfilename(
            title="Save Output PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not output_pdf:
            messagebox.showinfo(
                "No Save Location", "You must specify a location to save the new PDF."
            )
            return

        print(f"\nStarting to overlay {image_file} UNDER {pdf_file}")
        print("Opening PDF document...")

        pdf_document = fitz.open(pdf_file)
        total_pages = len(pdf_document)
        print(f"Found {total_pages} pages")

        # Load and prepare the overlay image
        overlay_image = Image.open(image_file)

        # Prepare a resized image for each page dynamically
        for page_number in range(total_pages):
            print(f"Processing page {page_number + 1}/{total_pages}")

            page = pdf_document[page_number]
            rect = page.rect  # page size in points (1 pt = 1/72 inch)

            page_width = rect.width
            page_height = rect.height
            print(f"Page size: {page_width} x {page_height} points")

            img_width, img_height = overlay_image.size
            img_aspect = img_width / img_height
            page_aspect = page_width / page_height

            # Calculate new image size maintaining aspect ratio
            if img_aspect > page_aspect:
                # Image is wider relative to page
                new_width = page_width
                new_height = page_width / img_aspect
            else:
                # Image is taller relative to page
                new_height = page_height
                new_width = page_height * img_aspect

            print(f"Resized image size: {new_width:.2f} x {new_height:.2f} points")

            # Resize the image
            resized_image = overlay_image.resize(
                (int(new_width), int(new_height)), Image.LANCZOS
            )

            # Convert resized image to bytes
            img_byte_arr = BytesIO()
            resized_image.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()

            # Calculate position to center the image
            x0 = (page_width - new_width) / 2
            y0 = (page_height - new_height) / 2
            x1 = x0 + new_width
            y1 = y0 + new_height

            # Insert the image UNDER existing content
            page.insert_image(
                fitz.Rect(x0, y0, x1, y1),
                stream=img_bytes,
                overlay=False,  # <<< False = place underneath
            )

        print(f"\nSaving new PDF to {output_pdf}...")
        pdf_document.save(output_pdf)
        pdf_document.close()

        print("Overlay under content completed successfully!")
        messagebox.showinfo(
            "Success", f"Overlay completed successfully!\nSaved as: {output_pdf}"
        )

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    overlay_image_under_pdf_content()
