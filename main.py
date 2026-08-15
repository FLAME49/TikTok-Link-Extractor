"""
TikTok Link Extractor — entry point.

Run with:
    python main.py
"""
import sys

from PySide6.QtWidgets import QApplication

from app.icon import get_app_icon
from app.main_window import TikTokExtractorApp


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(get_app_icon())

    window = TikTokExtractorApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
