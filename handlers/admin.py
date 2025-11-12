from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.database import Database
from utils.helpers import log_to_channel

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin statistics (for bot owner only)"""
    user = update.effective_user
    
    # Check if user is bot owner (you should set your user ID in config)
    if user.id != 123456789:  # Replace with your user ID
        await update.message.reply_text("❌ This command is for bot administrators only.")
        return

    db = Database()
    
    # Get total statistics
    async with db.conn.execute('SELECT COUNT(*) FROM users') as cursor:
        total_users = (await cursor.fetchone())[0]
    
    async with db.conn.execute('SELECT COUNT(*) FROM downloads') as cursor:
        total_downloads = (await cursor.fetchone())[0]
    
    async with db.conn.execute('SELECT SUM(file_size) FROM downloads') as cursor:
        total_data = (await cursor.fetchone())[0] or 0

    stats_text = f"""
👑 *Admin Statistics*

👥 Total Users: {total_users}
📥 Total Downloads: {total_downloads}
💾 Total Data: {await format_size(total_data)}
🟢 Bot Status: Online

*Recent Activity:*
• Last hour: N/A
• Last 24h: N/A
• Last 7d: N/A
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users (admin only)"""
    user = update.effective_user
    
    if user.id != 123456789:  # Replace with your user ID
        await update.message.reply_text("❌ This command is for bot administrators only.")
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /broadcast <message>")
        return

    message = ' '.join(context.args)
    db = Database()
    
    # Get all users
    async with db.conn.execute('SELECT user_id FROM users') as cursor:
        users = await cursor.fetchall()
    
    success = 0
    failed = 0
    
    for (user_id,) in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"📢 *Broadcast Message*\\n\\n{message}",
                parse_mode='Markdown'
            )
            success += 1
        except:
            failed += 1
    
    await update.message.reply_text(
        f"📢 Broadcast Complete\\n✅ Success: {success}\\n❌ Failed: {failed}",
        parse_mode='Markdown'
    )

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