import yt_dlp
import os
from datetime import datetime

class YouTubeDownloader:
    def __init__(self):
        self.output_dir = 'downloads/youtube'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, format_type):
        options = {
            'format': self._get_format_option(format_type),
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                return {
                    'status': 'success',
                    'title': info['title'],
                    'filename': ydl.prepare_filename(info),
                    'format': format_type
                }
            except Exception as e:
                raise Exception(f"YouTube download failed: {str(e)}")

    def _get_format_option(self, format_type):
        format_options = {
            'MP4 - 1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]',
            'MP4 - 720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]',
            'MP4 - 480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]',
            'MP3 Audio': 'bestaudio[ext=mp3]/best[ext=mp4]/best'
        }
        return format_options.get(format_type, 'best')

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = float(d['downloaded_bytes']) / float(d['total_bytes']) * 100
            print(f"Download Progress: {progress:.1f}%")