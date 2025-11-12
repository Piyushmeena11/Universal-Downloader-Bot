from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.database import Database
from utils.helpers import log_to_channel

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when the command /start is issued."""
    user = update.effective_user
    db = Database()
    
    # Add user to database
    await db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = f"""
👋 Hello *{user.first_name}*!

I'm *Universal Downloader Bot* 🚀

I can download videos and files from various platforms:

📹 *YouTube* - Videos & Shorts
📷 *Instagram* - Posts, Stories, Reels
📘 *Facebook* - Videos & Reels
🐦 *Twitter* - Videos & GIFs
🎵 *TikTok* - Videos without watermark
🔗 *Direct Links* - MP4, MKV, AVI, etc.

*How to use:* Simply send me the link you want to download!

⚡ *Features:*
• High speed downloads
• Multiple quality options  
• Support for various formats
• Personal log channel
• Large file support (up to 2GB)

Send me a link to get started! 🎯
    """
    
    keyboard = [
        [InlineKeyboardButton("📢 Support Channel", url="https://t.me/your_channel")],
        [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/your_username")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    # Log user start
    await log_to_channel(
        context.bot,
        f"🆕 New User Started Bot\n"
        f"👤 User: {user.first_name} (@{user.username})\n"
        f"🆔 ID: `{user.id}`",
        "info"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when the command /help is issued."""
    help_text = """
🤖 *Universal Downloader Bot Help*

*Supported Platforms:*
• YouTube (Videos, Shorts, Live)
• Instagram (Posts, Stories, Reels)
• Facebook (Videos, Reels)
• Twitter/X (Videos, GIFs)
• TikTok (Videos without watermark)
• Reddit (Videos)
• Pinterest (Videos)
• SoundCloud (Audio)
• Vimeo, Dailymotion
• Direct download links

*Available Commands:*
/start - Start the bot
/help - Show this help message
/stats - Show your download statistics
/settings - Configure bot settings

*How to Use:*
1. Send any supported link
2. Choose video quality (if available)
3. Wait for download to complete
4. Receive your file!

*Note:* 
• Maximum file size: 2GB
• Some DRM protected content may not be downloadable
• Download speed depends on your internet connection

Need help? Contact @your_username
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user = update.effective_user
    db = Database()
    
    download_count, total_size = await db.get_user_stats(user.id)
    
    stats_text = f"""
📊 *Your Download Statistics*

👤 User: {user.first_name}
📥 Total Downloads: {download_count}
💾 Total Data: {await format_size(total_size)}
🎯 Status: {'Active' if download_count > 0 else 'New User'}

Keep downloading! 🚀
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def format_size(size_bytes):
    """Format size in bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.2f} {size_names[i]}"