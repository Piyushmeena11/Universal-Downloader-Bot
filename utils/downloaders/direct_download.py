import aiohttp
import os
import asyncio
from config import Config
from utils.helpers import format_file_size, clean_filename, get_file_extension

class DirectDownloader:
    def __init__(self):
        self.chunk_size = 8192
        self.timeout = aiohttp.ClientTimeout(total=3600)  # 1 hour timeout

    async def download(self, url, custom_filename=None):
        """Download file from direct URL"""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Get filename
                        if custom_filename:
                            filename = custom_filename
                        else:
                            filename = self._get_filename_from_url(url, response)
                        
                        file_path = os.path.join(Config.DOWNLOAD_PATH, filename)
                        
                        # Create downloads directory if not exists
                        os.makedirs(Config.DOWNLOAD_PATH, exist_ok=True)
                        
                        file_size = int(response.headers.get('content-length', 0))
                        
                        # Check file size limit
                        if file_size > Config.MAX_FILE_SIZE:
                            return None, f"File size ({format_file_size(file_size)}) exceeds limit ({format_file_size(Config.MAX_FILE_SIZE)})"
                        
                        downloaded = 0
                        with open(file_path, 'wb') as file:
                            async for chunk in response.content.iter_chunked(self.chunk_size):
                                if chunk:
                                    file.write(chunk)
                                    downloaded += len(chunk)
                        
                        return file_path, {
                            'filename': filename,
                            'filesize': file_size,
                            'type': 'direct_download'
                        }
                    else:
                        return None, f"HTTP Error: {response.status}"
                        
        except asyncio.TimeoutError:
            return None, "Download timeout"
        except Exception as e:
            return None, f"Direct download error: {str(e)}"

    def _get_filename_from_url(self, url, response):
        """Extract filename from URL or response headers"""
        import re
        from urllib.parse import unquote, urlparse
        
        # Try Content-Disposition header first
        content_disposition = response.headers.get('Content-Disposition', '')
        if 'filename=' in content_disposition:
            filename = re.findall('filename="?(.+)"?', content_disposition)[0]
            return clean_filename(unquote(filename))
        
        # Extract from URL
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename or filename == '/':
            filename = f"download{get_file_extension(url)}"
        
        return clean_filename(unquote(filename))