"""
Central place for the app's "elegant night" color palette and Qt
stylesheets (QSS). Keeping colors and QSS here means every widget/dialog
draws from the same palette instead of scattering hex codes across the
codebase.
"""

# ----------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------
BG_MAIN = "#0B0E17"        # main window background
BG_CARD = "#151A28"        # card / dialog background
BG_INPUT = "#0F1420"       # text inputs / output box background
BORDER = "#262D40"         # default border
BORDER_LIGHT = "#2E3648"   # input border
BORDER_HOVER = "#333B52"   # secondary button hover

TEXT_PRIMARY = "#EDEFF5"   # main text
TEXT_SECONDARY = "#8B93A8"  # secondary / hint text
TEXT_MUTED = "#5A6178"     # disabled text
TEXT_LINKS = "#D9C89A"     # extracted links in the output box

ACCENT = "#C9A96A"         # champagne gold — primary accent
ACCENT_HOVER = "#D9BC85"
ACCENT_PRESSED = "#A37D3D"

SUCCESS = "#3FAE8B"
SUCCESS_HOVER = "#57C29E"
DANGER = "#E17070"
DANGER_HOVER = "#EF8B8B"
WARNING = "#D9A441"

# ----------------------------------------------------------------------
# Stylesheets
# ----------------------------------------------------------------------
MAIN_WINDOW_QSS = f"""
    QMainWindow {{
        background-color: {BG_MAIN};
    }}
    QFrame#card {{
        background-color: {BG_CARD};
        border-radius: 12px;
        border: 1px solid {BORDER};
    }}
    QLabel {{
        color: {TEXT_PRIMARY};
        font-family: 'Segoe UI', sans-serif;
    }}
    QLineEdit {{
        background-color: {BG_INPUT};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        selection-background-color: {ACCENT};
        selection-color: {BG_CARD};
    }}
    QLineEdit:focus {{
        border: 1px solid {ACCENT};
    }}
    QPushButton {{
        background-color: {ACCENT};
        color: {BG_CARD};
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 13px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {ACCENT_PRESSED};
    }}
    QPushButton:disabled {{
        background-color: {BORDER};
        color: {TEXT_MUTED};
    }}
    QPushButton#saveBtn {{
        background-color: {SUCCESS};
        color: {BG_MAIN};
    }}
    QPushButton#saveBtn:hover {{
        background-color: {SUCCESS_HOVER};
    }}
    QTextEdit {{
        background-color: {BG_INPUT};
        color: {TEXT_LINKS};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 10px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
    }}
    QProgressBar {{
        border: none;
        background-color: {BG_INPUT};
        height: 6px;
        border-radius: 3px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background-color: {ACCENT};
        border-radius: 3px;
    }}
"""

PROXY_DIALOG_QSS = f"""
    QDialog {{
        background-color: {BG_CARD};
        border: 1px solid {BORDER};
    }}
    QLabel {{
        color: {TEXT_PRIMARY};
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
    }}
    QLineEdit {{
        background-color: {BG_MAIN};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 12px;
    }}
    QLineEdit:focus {{
        border: 1px solid {ACCENT};
    }}
    QPushButton {{
        background-color: {ACCENT};
        color: {BG_CARD};
        border: none;
        border-radius: 6px;
        padding: 8px 14px;
        font-size: 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QPushButton#secondaryBtn {{
        background-color: {BORDER};
        color: {TEXT_PRIMARY};
    }}
    QPushButton#secondaryBtn:hover {{
        background-color: {BORDER_HOVER};
    }}
"""

COOKIE_BTN_DEFAULT_QSS = f"""
    QPushButton {{
        background-color: transparent;
        color: {TEXT_SECONDARY};
        border: none;
        border-radius: 0px;
        padding: 2px 0px;
        font-size: 11px;
        font-weight: 500;
        text-align: left;
    }}
    QPushButton:hover {{
        color: {ACCENT};
    }}
"""

COOKIE_BTN_ACTIVE_QSS = f"""
    QPushButton {{
        background-color: transparent;
        color: {SUCCESS};
        border: none;
        padding: 2px 0px;
        font-size: 11px;
        font-weight: 600;
        text-align: left;
    }}
    QPushButton:hover {{
        color: {SUCCESS_HOVER};
    }}
"""

COOKIE_CLEAR_BTN_QSS = f"""
    QPushButton {{
        background-color: transparent;
        color: {DANGER};
        border: none;
        padding: 2px 0px;
        font-size: 11px;
    }}
    QPushButton:hover {{
        color: {DANGER_HOVER};
    }}
"""


def optional_btn_style(color: str) -> str:
    """Style for the small flat 'optional setting' buttons (cookies /
    proxy) whose text color reflects whether a value is set."""
    return f"""
        QPushButton {{
            background-color: transparent;
            color: {color};
            border: none;
            padding: 2px 0px;
            font-size: 11px;
            font-weight: 500;
            text-align: left;
        }}
        QPushButton:hover {{
            color: {ACCENT};
        }}
    """
