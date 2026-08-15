"""
Background worker that extracts video links from a TikTok profile,
playlist, or single post using yt-dlp, without blocking the UI thread.
"""
import yt_dlp
from PySide6.QtCore import QThread, Signal

# A realistic desktop User-Agent makes TikTok far less likely to reject
# or throttle the request.
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
_HTTP_HEADERS = {
    "User-Agent": _USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}


class ExtractorThread(QThread):
    """Runs yt-dlp's flat extraction in a background thread and reports
    progress, the final list of URLs, or an error back to the UI via
    Qt signals."""

    progress_signal = Signal(str)
    finished_signal = Signal(list, str)
    error_signal = Signal(str)

    def __init__(self, target_url, cookie_file=None, proxy=None):
        super().__init__()
        self.target_url = target_url
        self.cookie_file = cookie_file
        self.proxy = proxy

    def run(self):
        self.progress_signal.emit("Analyzing URL and fetching video list...")

        # Yt-dlp options for flat extraction (fast, no heavy downloading).
        # 'in_playlist' (not True) keeps only the playlist/profile entries
        # flat, without yt-dlp trying to flatten anything else — this is
        # the mode that reliably works for TikTok listings.
        ydl_opts = {
            "extract_flat": "in_playlist",
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "user_agent": _USER_AGENT,
            "http_headers": _HTTP_HEADERS,
        }

        # Use Netscape-format cookies.txt if the user provided one
        if self.cookie_file:
            ydl_opts["cookiefile"] = self.cookie_file

        # Route requests through a proxy if the user provided one
        if self.proxy:
            ydl_opts["proxy"] = self.proxy

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(self.target_url, download=False)

                urls = []
                if result is None:
                    self.error_signal.emit("Failed to fetch data. Please check the URL.")
                    return

                # If playlist/profile context
                if "entries" in result:
                    entries = [e for e in result["entries"] if e]
                    total = len(entries)
                    for idx, entry in enumerate(entries, 1):
                        # Take the real URL as-is. Never fabricate one —
                        # a guessed/placeholder link just points to an
                        # invalid page and silently corrupts the output.
                        video_url = entry.get("url") or entry.get("webpage_url")
                        if video_url:
                            urls.append(video_url)
                        self.progress_signal.emit(f"Extracted {idx} / {total} videos...")
                else:
                    # Single video fallback
                    video_url = result.get("webpage_url") or result.get("url")
                    if video_url:
                        urls.append(video_url)

                title = result.get("title", "TikTok_Links")
                self.finished_signal.emit(urls, title)

        except Exception as e:
            self.error_signal.emit(f"Error: {str(e)}")
