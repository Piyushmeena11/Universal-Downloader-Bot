import yt_dlp
import os
import asyncio
from threading import Thread
from config import Config
from utils.helpers import format_file_size, clean_filename

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': os.path.join(Config.DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'noplaylist': True,
        }

    async def download(self, url, quality='720p'):
        """Download video from YouTube and similar platforms"""
        try:
            # Update format based on quality
            if quality == '1080p':
                self.ydl_opts['format'] = 'best[height<=1080]'
            elif quality == '480p':
                self.ydl_opts['format'] = 'best[height<=480]'
            elif quality == '360p':
                self.ydl_opts['format'] = 'best[height<=360]'
            elif quality == 'audio':
                self.ydl_opts['format'] = 'bestaudio'
                self.ydl_opts['extractaudio'] = True
                self.ydl_opts['audioformat'] = 'mp3'

            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, self._get_video_info, url)
            
            if not info:
                return None, "Failed to get video information"

            file_path = await loop.run_in_executor(None, self._download_video, url)
            
            return file_path, info

        except Exception as e:
            return None, f"YouTube download error: {str(e)}"

    def _get_video_info(self, url):
        """Get video information"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'thumbnail': info.get('thumbnail', ''),
                    'filesize': info.get('filesize', 0) or info.get('filesize_approx', 0)
                }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def _download_video(self, url):
        """Download video"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None