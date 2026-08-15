"""
Main application window: URL input, optional cookies/proxy settings,
progress/status feedback, and the extracted-links output box.
"""
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QProgressBar, QPushButton, QTextEdit, QVBoxLayout, QWidget,
)

from . import theme
from .extractor_thread import ExtractorThread
from .icon import get_app_icon
from .proxy_dialog import ProxyDialog


class TikTokExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.extracted_urls = []
        self.cookie_file_path = None
        self.proxy_address = ""
        self.thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TikTok Link Extractor")
        self.setWindowIcon(get_app_icon())
        self.resize(680, 520)
        self.setMinimumSize(600, 480)

        self.setStyleSheet(theme.MAIN_WINDOW_QSS)

        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Card Container
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(16)

        # Title Section
        header_title = QLabel("TikTok Link Extractor")
        header_title.setFont(QFont("Segoe UI", 18, QFont.Bold))

        header_sub = QLabel("Extract pure video URLs from user profiles, playlists, or single posts.")
        header_sub.setStyleSheet(f"color: {theme.TEXT_SECONDARY}; font-size: 12px;")

        card_layout.addWidget(header_title)
        card_layout.addWidget(header_sub)

        # Input Layout
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste TikTok Profile or Playlist URL here...")

        self.extract_btn = QPushButton("Extract Links")
        self.extract_btn.setCursor(Qt.PointingHandCursor)
        self.extract_btn.clicked.connect(self.start_extraction)

        input_layout.addWidget(self.url_input, stretch=4)
        input_layout.addWidget(self.extract_btn, stretch=1)
        card_layout.addLayout(input_layout)

        # Cookie File Layout (optional, Netscape cookies.txt)
        cookie_row = QHBoxLayout()
        cookie_row.setContentsMargins(0, 0, 0, 0)
        cookie_row.setSpacing(6)

        self.cookie_btn = QPushButton("🍪  Add cookies.txt (optional)")
        self.cookie_btn.setCursor(Qt.PointingHandCursor)
        self.cookie_btn.setFlat(True)
        self.cookie_btn.setStyleSheet(theme.COOKIE_BTN_DEFAULT_QSS)
        self.cookie_btn.clicked.connect(self.browse_cookie_file)

        self.cookie_clear_btn = QPushButton("✕")
        self.cookie_clear_btn.setCursor(Qt.PointingHandCursor)
        self.cookie_clear_btn.setFlat(True)
        self.cookie_clear_btn.setFixedWidth(18)
        self.cookie_clear_btn.setStyleSheet(theme.COOKIE_CLEAR_BTN_QSS)
        self.cookie_clear_btn.clicked.connect(self.clear_cookie_file)
        self.cookie_clear_btn.hide()

        # Small separator dot between the two optional settings
        sep_label = QLabel("·")
        sep_label.setStyleSheet(f"color: {theme.BORDER_HOVER}; font-size: 11px;")

        self.proxy_btn = QPushButton("🌐  Add proxy (optional)")
        self.proxy_btn.setCursor(Qt.PointingHandCursor)
        self.proxy_btn.setFlat(True)
        self.proxy_btn.setStyleSheet(theme.optional_btn_style(theme.TEXT_SECONDARY))
        self.proxy_btn.clicked.connect(self.open_proxy_dialog)

        cookie_row.addWidget(self.cookie_btn)
        cookie_row.addWidget(self.cookie_clear_btn)
        cookie_row.addWidget(sep_label)
        cookie_row.addWidget(self.proxy_btn)
        cookie_row.addStretch()
        card_layout.addLayout(cookie_row)

        # Progress Bar & Status
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate initially
        self.progress_bar.hide()
        card_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {theme.TEXT_SECONDARY}; font-size: 12px; font-weight: 500;")
        card_layout.addWidget(self.status_label)

        # Output Preview Box
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Extracted video links will appear here...")
        card_layout.addWidget(self.output_box)

        # Bottom Action Layout
        bottom_layout = QHBoxLayout()
        self.count_label = QLabel("Total Links: 0")
        self.count_label.setStyleSheet(f"color: {theme.TEXT_SECONDARY}; font-weight: bold;")

        self.save_btn = QPushButton("Save to TXT")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_to_file)

        bottom_layout.addWidget(self.count_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.save_btn)

        card_layout.addLayout(bottom_layout)
        main_layout.addWidget(card)

    # ------------------------------------------------------------------
    # Cookies
    # ------------------------------------------------------------------
    def browse_cookie_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select cookies.txt (Netscape format)",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.cookie_file_path = file_path
            display_name = os.path.basename(file_path)
            if len(display_name) > 28:
                display_name = display_name[:25] + "..."
            self.cookie_btn.setText(f"🍪  {display_name}")
            self.cookie_btn.setStyleSheet(theme.COOKIE_BTN_ACTIVE_QSS)
            self.cookie_clear_btn.show()

    def clear_cookie_file(self):
        self.cookie_file_path = None
        self.cookie_btn.setText("🍪  Add cookies.txt (optional)")
        self.cookie_btn.setStyleSheet(theme.COOKIE_BTN_DEFAULT_QSS)
        self.cookie_clear_btn.hide()

    # ------------------------------------------------------------------
    # Proxy
    # ------------------------------------------------------------------
    def open_proxy_dialog(self):
        dialog = ProxyDialog(self, current_proxy=self.proxy_address)
        dialog.exec()
        self.proxy_address = dialog.result_proxy

        if self.proxy_address:
            display = self.proxy_address
            if len(display) > 26:
                display = display[:23] + "..."
            self.proxy_btn.setText(f"🌐  {display}")
            self.proxy_btn.setStyleSheet(theme.optional_btn_style(theme.SUCCESS))
        else:
            self.proxy_btn.setText("🌐  Add proxy (optional)")
            self.proxy_btn.setStyleSheet(theme.optional_btn_style(theme.TEXT_SECONDARY))

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------
    def start_extraction(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a valid URL first.")
            self.status_label.setStyleSheet(f"color: {theme.DANGER};")
            return

        # Interface State: Processing
        self.extract_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.output_box.clear()
        self.extracted_urls.clear()
        self.count_label.setText("Total Links: 0")
        self.progress_bar.show()
        self.status_label.setStyleSheet(f"color: {theme.ACCENT};")

        # Thread Start
        self.thread = ExtractorThread(url, cookie_file=self.cookie_file_path, proxy=self.proxy_address or None)
        self.thread.progress_signal.connect(self.update_status)
        self.thread.finished_signal.connect(self.extraction_finished)
        self.thread.error_signal.connect(self.extraction_failed)
        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def extraction_finished(self, urls, title):
        self.extracted_urls = urls
        self.progress_bar.hide()
        self.extract_btn.setEnabled(True)

        if not urls:
            self.status_label.setText("No videos found in the provided URL.")
            self.status_label.setStyleSheet(f"color: {theme.WARNING};")
            return

        # Render clean text output (one link per line)
        self.output_box.setText("\n".join(urls))
        self.count_label.setText(f"Total Links: {len(urls)}")
        self.status_label.setText("Extraction completed successfully!")
        self.status_label.setStyleSheet(f"color: {theme.SUCCESS};")
        self.save_btn.setEnabled(True)

    def extraction_failed(self, error_msg):
        self.progress_bar.hide()
        self.extract_btn.setEnabled(True)
        self.status_label.setText(error_msg)
        self.status_label.setStyleSheet(f"color: {theme.DANGER};")

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    def save_to_file(self):
        if not self.extracted_urls:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Links File",
            "tiktok_links.txt",
            "Text Files (*.txt)"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    for link in self.extracted_urls:
                        f.write(f"{link}\n")
                self.status_label.setText(f"File saved successfully to: {os.path.basename(file_path)}")
                self.status_label.setStyleSheet(f"color: {theme.SUCCESS};")
            except Exception as e:
                self.status_label.setText(f"Failed to save file: {str(e)}")
                self.status_label.setStyleSheet(f"color: {theme.DANGER};")
