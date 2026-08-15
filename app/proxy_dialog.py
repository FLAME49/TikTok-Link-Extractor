"""
Small popup dialog for setting an HTTP/SOCKS proxy address, either typed
manually or loaded from a .txt file.
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QVBoxLayout,
)

from . import theme


class ProxyDialog(QDialog):
    """Lets the user type a proxy address or load the first line of a
    .txt file as the proxy address."""

    def __init__(self, parent=None, current_proxy=""):
        super().__init__(parent)
        self.setWindowTitle("Proxy Settings")
        self.setFixedSize(360, 160)
        self.setStyleSheet(theme.PROXY_DIALOG_QSS)

        self.result_proxy = current_proxy

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QLabel("🌐 Proxy")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(title)

        hint = QLabel("Enter proxy address, or load from a .txt file")
        hint.setStyleSheet(f"color: {theme.TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(hint)

        input_row = QHBoxLayout()
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://user:pass@host:port")
        self.proxy_input.setText(current_proxy)
        self.load_btn = QPushButton("📂")
        self.load_btn.setFixedWidth(36)
        self.load_btn.setObjectName("secondaryBtn")
        self.load_btn.setCursor(Qt.PointingHandCursor)
        self.load_btn.clicked.connect(self.load_from_file)
        input_row.addWidget(self.proxy_input, stretch=1)
        input_row.addWidget(self.load_btn)
        layout.addLayout(input_row)

        layout.addStretch()

        btn_row = QHBoxLayout()
        self.clear_btn = QPushButton("Remove Proxy")
        self.clear_btn.setObjectName("secondaryBtn")
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.remove_proxy)

        self.save_btn = QPushButton("Save")
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_and_close)

        btn_row.addWidget(self.clear_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

    def load_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select proxy .txt file",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    # Use the first non-empty line as the proxy address
                    for line in f:
                        line = line.strip()
                        if line:
                            self.proxy_input.setText(line)
                            break
            except Exception:
                pass

    def remove_proxy(self):
        self.proxy_input.clear()
        self.result_proxy = ""
        self.accept()

    def save_and_close(self):
        self.result_proxy = self.proxy_input.text().strip()
        self.accept()
