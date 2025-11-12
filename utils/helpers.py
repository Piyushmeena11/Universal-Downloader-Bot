import os
import logging
from datetime import datetime
from config import Config

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def log_to_channel(bot, message, message_type="info"):
    """Send log message to personal log channel"""
    try:
        if Config.LOG_CHANNEL_ID:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            emoji = "ℹ️"
            if message_type == "error":
                emoji = "❌"
            elif message_type == "success":
                emoji = "✅"
            elif message_type == "warning":
                emoji = "⚠️"
                
            log_message = f"{emoji} *Log Entry* - `{timestamp}`\n\n{message}"
            
            await bot.send_message(
                chat_id=Config.LOG_CHANNEL_ID,
                text=log_message,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Failed to send log to channel: {e}")

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.2f} {size_names[i]}"

def is_supported_url(url):
    """Check if the URL is supported by the bot"""
    import re
    domain_pattern = r'https?://([^/]+)'
    match = re.search(domain_pattern, url)
    
    if match:
        domain = match.group(1).lower()
        for supported_domain in Config.SUPPORTED_DOMAINS:
            if supported_domain in domain:
                return True
    return False

def clean_filename(filename):
    """Clean filename to remove invalid characters"""
    import re
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return filename[:255]  # Limit filename length

def get_file_extension(url):
    """Extract file extension from URL"""
    import os
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    root, ext = os.path.splitext(parsed.path)
    return ext.lower() if ext else '.mp4'