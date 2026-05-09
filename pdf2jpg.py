import sys
import os
import zipfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QProgressBar, QFrame, QPushButton, QHBoxLayout,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QFont, QColor, QPalette

class PDFConverterThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, str) # success, message, folder_path

    def __init__(self, pdf_files):
        super().__init__()
        self.pdf_files = pdf_files

    def run(self):
        try:
            import fitz  # Lazy load
            total_files = len(self.pdf_files)
            last_output_dir = ""
            
            for file_idx, pdf_file in enumerate(self.pdf_files):
                base_msg = f"[{file_idx + 1}/{total_files}] {os.path.basename(pdf_file)}"
                self.progress.emit(int((file_idx / total_files) * 100), f"{base_msg}: Opening...")
                
                # Create a directory to store the JPG files
                output_dir = os.path.splitext(pdf_file)[0] + "_images"
                os.makedirs(output_dir, exist_ok=True)
                last_output_dir = output_dir

                # Open the PDF using PyMuPDF
                doc = fitz.open(pdf_file)
                total_pages = len(doc)

                # Save each page as a JPG file
                for i in range(total_pages):
                    page = doc.load_page(i)
                    pix = page.get_pixmap()
                    image_path = os.path.join(output_dir, f"page_{i + 1}.jpg")
                    pix.save(image_path)
                    
                    # Calculate progress: current file contribution + current page contribution
                    file_progress = (file_idx / total_files) * 100
                    page_progress = ((i + 1) / total_pages) * (100 / total_files) * 0.8 # 80% for conversion
                    self.progress.emit(int(file_progress + page_progress), f"{base_msg}: Page {i+1}/{total_pages}")

                doc.close()

                # Archive images into a zip file
                self.progress.emit(int(file_progress + (100/total_files)*0.9), f"{base_msg}: Archiving...")
                zip_filename = os.path.splitext(pdf_file)[0] + "_images.zip"
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for root, _, files in os.walk(output_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, output_dir)
                            zipf.write(file_path, arcname=arcname)

            self.progress.emit(100, "Done!")
            self.finished.emit(True, f"Successfully converted {total_files} PDF(s).", os.path.dirname(self.pdf_files[0]))

        except Exception as e:
            self.finished.emit(False, str(e), "")

class DropZone(QFrame):
    filesDropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setObjectName("DropZone")
        
        layout = QVBoxLayout(self)
        self.label = QLabel("Drag & Drop PDF(s) here\nor click to browse")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #888; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.label)

        self.default_style = """
            #DropZone {
                border: 2px dashed #555;
                border-radius: 15px;
                background-color: #222;
            }
        """
        self.hover_style = """
            #DropZone {
                border: 2px dashed #0078d4;
                background-color: #2a2a2a;
            }
        """
        self.setStyleSheet(self.default_style)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith(".pdf") for url in urls):
                event.accept()
                self.setStyleSheet(self.hover_style)
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet(self.default_style)
        files = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().lower().endswith(".pdf")]
        if files:
            self.filesDropped.emit(files)

    def mousePressEvent(self, event):
        files, _ = QFileDialog.getOpenFileNames(self, "Open PDF(s)", "", "PDF Files (*.pdf)")
        if files:
            self.filesDropped.emit(files)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to JPG Converter")
        self.setMinimumSize(500, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Title
        self.title_label = QLabel("PDF to JPG")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #fff;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Drop Zone
        self.drop_zone = DropZone()
        self.drop_zone.filesDropped.connect(self.start_conversion)
        self.layout.addWidget(self.drop_zone)

        # Progress Area
        self.progress_container = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_container)
        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #aaa;")
        self.progress_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 5px;
                background-color: #333;
                text-align: center;
                height: 10px;
                color: transparent;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 5px;
            }
        """)
        self.progress_bar.setValue(0)
        self.progress_layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.progress_container)
        self.progress_container.hide()

        # Success Buttons
        self.buttons_container = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_container)
        self.btn_open_folder = QPushButton("Open Folder")
        self.btn_open_folder.clicked.connect(self.open_output_folder)
        self.btn_reset = QPushButton("Convert Another")
        self.btn_reset.clicked.connect(self.reset_ui)
        self.buttons_layout.addWidget(self.btn_open_folder)
        self.buttons_layout.addWidget(self.btn_reset)
        self.layout.addWidget(self.buttons_container)
        self.buttons_container.hide()

        self.last_output_dir = ""
        self.set_dark_theme()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(18, 18, 18))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        self.setPalette(palette)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QPushButton {
                background-color: #333;
                border: none;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #444; }
        """)

    def start_conversion(self, files):
        self.drop_zone.hide()
        self.progress_container.show()
        self.status_label.setText(f"Preparing {len(files)} file(s)...")
        self.progress_bar.setValue(0)
        
        self.thread = PDFConverterThread(files)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.status_label.setText(msg)

    def conversion_finished(self, success, message, folder_path):
        if success:
            self.last_output_dir = folder_path
            self.status_label.setText("Conversion Complete!")
            self.buttons_container.show()
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{message}")
            self.reset_ui()

    def open_output_folder(self):
        if self.last_output_dir and os.path.exists(self.last_output_dir):
            os.startfile(self.last_output_dir)

    def reset_ui(self):
        self.buttons_container.hide()
        self.progress_container.hide()
        self.drop_zone.show()
        self.status_label.setText("Ready")
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
