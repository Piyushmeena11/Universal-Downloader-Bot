import yt_dlp
import os
import asyncio
from config import Config
from utils.helpers import clean_filename

class SocialMediaDownloader:
    def __init__(self):
        self.ydl_opts = {
            'outtmpl': os.path.join(Config.DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

    async def download_instagram(self, url):
        """Download Instagram content"""
        try:
            self.ydl_opts['format'] = 'best'
            return await self._download_with_ytdlp(url)
        except Exception as e:
            return None, f"Instagram download error: {str(e)}"

    async def download_facebook(self, url):
        """Download Facebook video"""
        try:
            self.ydl_opts['format'] = 'best[height<=720]'
            return await self._download_with_ytdlp(url)
        except Exception as e:
            return None, f"Facebook download error: {str(e)}"

    async def download_tiktok(self, url):
        """Download TikTok video"""
        try:
            self.ydl_opts['format'] = 'best'
            return await self._download_with_ytdlp(url)
        except Exception as e:
            return None, f"TikTok download error: {str(e)}"

    async def download_twitter(self, url):
        """Download Twitter video"""
        try:
            self.ydl_opts['format'] = 'best'
            return await self._download_with_ytdlp(url)
        except Exception as e:
            return None, f"Twitter download error: {str(e)}"

    async def _download_with_ytdlp(self, url):
        """Generic download method using yt-dlp"""
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, self._get_video_info, url)
            
            if not info:
                return None, "Failed to get video information"

            file_path = await loop.run_in_executor(None, self._download_content, url)
            
            return file_path, info

        except Exception as e:
            return None, f"Social media download error: {str(e)}"

    def _get_video_info(self, url):
        """Get video information"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Social Media Video'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'thumbnail': info.get('thumbnail', ''),
                    'filesize': info.get('filesize', 0) or info.get('filesize_approx', 0),
                    'platform': info.get('extractor', 'social_media')
                }
        except Exception:
            return None

    def _download_content(self, url):
        """Download content"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        except Exception:
            return None