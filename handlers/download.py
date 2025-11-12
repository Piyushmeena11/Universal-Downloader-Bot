import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import Config
from utils.downloaders import YouTubeDownloader, DirectDownloader, SocialMediaDownloader, DRMHandler
from utils.database import Database
from utils.helpers import log_to_channel, format_file_size, is_supported_url

class DownloadHandler:
    def __init__(self):
        self.yt_downloader = YouTubeDownloader()
        self.direct_downloader = DirectDownloader()
        self.social_downloader = SocialMediaDownloader()
        self.drm_handler = DRMHandler()
        self.db = Database()

    async def handle_download(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle download requests"""
        user = update.effective_user
        message = update.message
        url = message.text.strip()

        # Validate URL
        if not await self._validate_url(url, update):
            return

        # Check if URL is supported
        if not is_supported_url(url) and not url.startswith(('http://', 'https://')):
            await message.reply_text("❌ *Unsupported URL*\\n\\nPlease provide a valid URL from supported platforms\\.", parse_mode='Markdown')
            return

        # Log download attempt
        await log_to_channel(
            context.bot,
            f"🔗 Download Request\\n👤 User: {user\\.first_name} \\(@{user\\.username or 'N/A'}\\)\\n🌐 URL: `{url}`",
            "info"
        )

        # Show processing message
        processing_msg = await message.reply_text("🔄 *Processing your request\\.\\.\\.*", parse_mode='Markdown')

        try:
            # Determine download type and process
            file_path, info, error = await self._process_download(url, user.id)

            if error:
                await processing_msg.edit_text(f"❌ *Download Failed*\\n\\n{error}")
                await log_to_channel(
                    context.bot,
                    f"❌ Download Failed\\n👤 User: {user\\.first_name}\\n🌐 URL: `{url}`\\n📝 Error: {error}",
                    "error"
                )
                return

            # Send file to user
            await self._send_file_to_user(message, file_path, info, context)

            # Update database
            await self.db.add_download(
                user_id=user.id,
                file_url=url,
                file_name=info.get('filename', 'Unknown'),
                file_size=info.get('filesize', 0)
            )

            # Clean up file
            if os.path.exists(file_path):
                os.remove(file_path)

            await processing_msg.delete()

        except Exception as e:
            await processing_msg.edit_text("❌ *An error occurred during download\\. Please try again\\.*")
            await log_to_channel(
                context.bot,
                f"💥 Unexpected Error\\n👤 User: {user\\.first_name}\\n🌐 URL: `{url}`\\n📝 Error: {str(e)}",
                "error"
            )

    async def _process_download(self, url, user_id):
        """Process download based on URL type"""
        # Check for DRM first
        if self.drm_handler.is_drm_protected(url):
            file_path, info = await self.drm_handler.handle_drm_content(url, user_id)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "DRM protected content cannot be downloaded"

        # YouTube and similar
        if any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            file_path, info = await self.yt_downloader.download(url)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "Failed to download YouTube content"

        # Instagram
        elif 'instagram.com' in url.lower():
            file_path, info = await self.social_downloader.download_instagram(url)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "Failed to download Instagram content"

        # Facebook
        elif 'facebook.com' in url.lower():
            file_path, info = await self.social_downloader.download_facebook(url)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "Failed to download Facebook content"

        # TikTok
        elif 'tiktok.com' in url.lower():
            file_path, info = await self.social_downloader.download_tiktok(url)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "Failed to download TikTok content"

        # Twitter
        elif 'twitter.com' in url.lower() or 'x.com' in url.lower():
            file_path, info = await self.social_downloader.download_twitter(url)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "Failed to download Twitter content"

        # Direct download
        else:
            file_path, info = await self.direct_downloader.download(url)
            if file_path:
                return file_path, info, None
            else:
                return None, None, "Failed to download from direct link"

    async def _send_file_to_user(self, message, file_path, info, context):
        """Send downloaded file to user"""
        file_size = os.path.getsize(file_path)
        
        # Prepare caption
        caption = f"✅ *Download Complete!*\n\n"
        caption += f"📁 *File:* {info.get('title', info.get('filename', 'Unknown'))}\n"
        caption += f"💾 *Size:* {format_file_size(file_size)}\n"
        
        if info.get('duration'):
            caption += f"⏱️ *Duration:* {info.get('duration')}s\n"
        
        if info.get('uploader'):
            caption += f"👤 *Uploader:* {info.get('uploader')}\n"

        # Determine file type and send
        if file_path.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.webm')):
            await message.reply_video(
                video=open(file_path, 'rb'),
                caption=caption,
                parse_mode='Markdown'
            )
        elif file_path.lower().endswith(('.mp3', '.m4a', '.wav', '.flac')):
            await message.reply_audio(
                audio=open(file_path, 'rb'),
                caption=caption,
                parse_mode='Markdown'
            )
        else:
            await message.reply_document(
                document=open(file_path, 'rb'),
                caption=caption,
                parse_mode='Markdown'
            )

        # Log successful download
        await log_to_channel(
            context.bot,
            f"✅ Download Successful\\n📁 File: {info\\.get('filename', 'Unknown')}\\n💾 Size: {format_file_size(file_size)}",
            "success"
        )

    async def _validate_url(self, url, update):
        """Validate the provided URL"""
        if not url:
            await update.message.reply_text("❌ Please provide a valid URL")
            return False

        if not url.startswith(('http://', 'https://')):
            await update.message.reply_text("❌ Invalid URL format. Please include http:// or https://")
            return False

        return True

# Create handler instance
download_handler = DownloadHandler()

# Export the main handler function
handle_download = download_handler.handle_download