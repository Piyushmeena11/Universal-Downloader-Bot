import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    BOT_USERNAME = os.getenv('BOT_USERNAME', '')
    
    # Channel Configuration
    LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID', '')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
    
    # Download Configuration
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 2147483648))  # 2GB
    DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', 'downloads')
    MAX_CONCURRENT_DOWNLOADS = int(os.getenv('MAX_CONCURRENT_DOWNLOADS', 3))
    
    # Heroku Configuration
    PORT = int(os.getenv('PORT', 8443))
    APP_URL = os.getenv('APP_URL', '')
    
    # Supported Domains
    SUPPORTED_DOMAINS = [
        'youtube.com', 'youtu.be', 'instagram.com', 'facebook.com',
        'twitter.com', 'tiktok.com', 'vimeo.com', 'dailymotion.com',
        'reddit.com', 'linkedin.com', 'pinterest.com', 'snapchat.com',
        'twitch.tv', 'soundcloud.com', 'spotify.com', 'deezer.com'
    ]