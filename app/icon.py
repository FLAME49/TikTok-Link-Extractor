"""
Embedded application icon.

The icon is stored directly as base64 PNG data instead of an external
file on purpose: an external assets/icon.ico file is fragile — it can
end up in the wrong folder relative to the script/exe, get skipped
during a copy, or get masked by a stale Windows icon-cache entry that
keeps showing an old/default icon even after the real file is fixed.
Embedding the icon as data means the window/taskbar icon always
renders correctly, regardless of where the app is run from or how
it's packaged.
"""
import base64

from PySide6.QtGui import QIcon, QPixmap

# A small dark-navy / champagne-gold "chain link" glyph matching the
# app's night theme.
_APP_ICON_BASE64 = (
    "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"
)


def get_app_icon() -> QIcon:
    """Decode the embedded icon into a QIcon. Safe to call multiple
    times; returns a blank QIcon (never raises) if decoding ever fails.
    """
    try:
        icon_bytes = base64.b64decode(_APP_ICON_BASE64)
        pixmap = QPixmap()
        if pixmap.loadFromData(icon_bytes, "PNG"):
            return QIcon(pixmap)
    except Exception:
        pass
    return QIcon()
