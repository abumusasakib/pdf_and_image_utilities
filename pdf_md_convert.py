import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QProgressBar, QFrame, QPushButton, QHBoxLayout,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QColor, QPalette

class ConverterThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, str) # success, message, file_path

    def __init__(self, input_files):
        super().__init__()
        self.input_files = input_files

    def run(self):
        try:
            total_files = len(self.input_files)
            last_file_path = ""
            
            for file_idx, input_file in enumerate(self.input_files):
                base_msg = f"[{file_idx + 1}/{total_files}] {os.path.basename(input_file)}"
                ext = os.path.splitext(input_file)[1].lower()
                
                # Calculate base progress for this file
                base_progress = int((file_idx / total_files) * 100)
                self.progress.emit(base_progress, f"{base_msg}: Starting...")

                if ext == ".md":
                    self.convert_md_to_pdf(input_file, base_progress, 100 // total_files, base_msg)
                elif ext == ".pdf":
                    self.convert_pdf_to_md(input_file, base_progress, 100 // total_files, base_msg)
                
                last_file_path = input_file

            self.progress.emit(100, "Done!")
            self.finished.emit(True, f"Successfully processed {total_files} file(s).", os.path.dirname(last_file_path))

        except Exception as e:
            self.finished.emit(False, str(e), "")

    def convert_md_to_pdf(self, input_file, base_prog, step_prog, base_msg):
        from markdown_pdf import MarkdownPdf, Section
        self.progress.emit(base_prog + int(step_prog * 0.2), f"{base_msg}: Reading Markdown...")
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        output_file = os.path.splitext(input_file)[0] + ".pdf"
        self.progress.emit(base_prog + int(step_prog * 0.5), f"{base_msg}: Rendering PDF...")
        
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

    def convert_pdf_to_md(self, input_file, base_prog, step_prog, base_msg):
        import pymupdf4llm
        self.progress.emit(base_prog + int(step_prog * 0.3), f"{base_msg}: Analyzing PDF...")
        output_file = os.path.splitext(input_file)[0] + ".md"
        
        self.progress.emit(base_prog + int(step_prog * 0.6), f"{base_msg}: Extracting Text...")
        md_text = pymupdf4llm.to_markdown(input_file)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_text)

class DropZone(QFrame):
    filesDropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setObjectName("DropZone")
        
        layout = QVBoxLayout(self)
        self.label = QLabel("Drag & Drop PDF or Markdown file(s) here\nor click to browse")
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
            if any(os.path.splitext(url.toLocalFile())[1].lower() in [".pdf", ".md"] for url in urls):
                event.accept()
                self.setStyleSheet(self.hover_style)
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet(self.default_style)
        files = [url.toLocalFile() for url in event.mimeData().urls() if os.path.splitext(url.toLocalFile())[1].lower() in [".pdf", ".md"]]
        if files:
            self.filesDropped.emit(files)

    def mousePressEvent(self, event):
        files, _ = QFileDialog.getOpenFileNames(self, "Open File(s)", "", "Supported Files (*.pdf *.md)")
        if files:
            self.filesDropped.emit(files)

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
        
        self.thread = ConverterThread(files)
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
