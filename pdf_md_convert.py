import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QProgressBar, QFrame, QPushButton, QHBoxLayout,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QPalette
from markdown_pdf import MarkdownPdf, Section
import pymupdf4llm

class ConverterThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, str) # success, message, file_path

    def __init__(self, input_file):
        super().__init__()
        self.input_file = input_file

    def run(self):
        try:
            ext = os.path.splitext(self.input_file)[1].lower()
            
            if ext == ".md":
                self.convert_md_to_pdf()
            elif ext == ".pdf":
                self.convert_pdf_to_md()
            else:
                self.finished.emit(False, "Unsupported file format. Please drop a .pdf or .md file.", "")

        except Exception as e:
            self.finished.emit(False, str(e), "")

    def convert_md_to_pdf(self):
        self.progress.emit(20, "Reading Markdown...")
        with open(self.input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        output_file = os.path.splitext(self.input_file)[0] + ".pdf"
        self.progress.emit(50, "Rendering PDF...")
        
        pdf = MarkdownPdf(toc_level=2, optimize=True)
        pdf.add_section(
            Section(content, toc=True),
            user_css="""
                h1, h2, h3 { font-family: Arial, sans-serif; }
                pre, code { background-color: #f4f4f4; padding: 5px; border-radius: 3px; font-family: monospace; }
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; }
            """
        )
        pdf.save(output_file)
        
        self.progress.emit(100, "Done!")
        self.finished.emit(True, f"Converted Markdown to PDF successfully.\nSaved as: {os.path.basename(output_file)}", output_file)

    def convert_pdf_to_md(self):
        self.progress.emit(30, "Analyzing PDF structure...")
        output_file = os.path.splitext(self.input_file)[0] + ".md"
        
        self.progress.emit(60, "Extracting text as Markdown...")
        # pymupdf4llm provides high-quality markdown extraction
        md_text = pymupdf4llm.to_markdown(self.input_file)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_text)
            
        self.progress.emit(100, "Done!")
        self.finished.emit(True, f"Converted PDF to Markdown successfully.\nSaved as: {os.path.basename(output_file)}", output_file)

class DropZone(QFrame):
    fileDropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setObjectName("DropZone")
        
        layout = QVBoxLayout(self)
        self.label = QLabel("Drag & Drop PDF or Markdown here\nor click to browse")
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
            url = event.mimeData().urls()[0].toLocalFile()
            ext = os.path.splitext(url)[1].lower()
            if ext in [".pdf", ".md"]:
                event.accept()
                self.setStyleSheet(self.hover_style)
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet(self.default_style)
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.fileDropped.emit(file_path)

    def mousePressEvent(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Supported Files (*.pdf *.md)")
        if file_path:
            self.fileDropped.emit(file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF & Markdown Converter")
        self.setMinimumSize(500, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)

        # Title
        self.title_label = QLabel("PDF & Markdown")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #fff;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Drop Zone
        self.drop_zone = DropZone()
        self.drop_zone.fileDropped.connect(self.start_conversion)
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
        self.btn_open_file = QPushButton("Open File")
        self.btn_open_file.clicked.connect(self.open_file)
        self.btn_reset = QPushButton("Convert Another")
        self.btn_reset.clicked.connect(self.reset_ui)
        self.buttons_layout.addWidget(self.btn_open_file)
        self.buttons_layout.addWidget(self.btn_reset)
        self.layout.addWidget(self.buttons_container)
        self.buttons_container.hide()

        self.last_output_file = ""
        self.set_dark_theme()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
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

    def start_conversion(self, file_path):
        self.drop_zone.hide()
        self.progress_container.show()
        self.status_label.setText(f"Processing: {os.path.basename(file_path)}")
        self.progress_bar.setValue(0)
        
        self.thread = ConverterThread(file_path)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.status_label.setText(msg)

    def conversion_finished(self, success, message, file_path):
        if success:
            self.last_output_file = file_path
            self.status_label.setText("Conversion Complete!")
            self.buttons_container.show()
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{message}")
            self.reset_ui()

    def open_file(self):
        if self.last_output_file and os.path.exists(self.last_output_file):
            os.startfile(self.last_output_file)

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
