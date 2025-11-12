# Universal Downloader Bot 🤖

A powerful Telegram bot that can download videos and files from various platforms with high speed and DRM support.

## Features ✨

- 📹 **Multi-Platform Support**: YouTube, Instagram, Facebook, Twitter, TikTok, etc.
- 🔒 **DRM Support**: Limited support for DRM protected content
- ⚡ **High Speed**: Optimized downloading with multiple threads
- 📊 **Personal Log Channel**: Track all downloads and user activities
- 🚀 **Heroku Deployable**: Easy deployment on Heroku
- 💾 **Large Files**: Support up to 2GB files
- 📱 **User-Friendly**: Simple interface with progress updates

## Supported Platforms 🌐

- YouTube (Videos, Shorts, Live)
- Instagram (Posts, Stories, Reels)
- Facebook (Videos, Reels)
- Twitter/X (Videos, GIFs)
- TikTok (Videos without watermark)
- Reddit, Pinterest, LinkedIn
- SoundCloud, Spotify, Deezer
- Vimeo, Dailymotion, Twitch
- Direct download links

## Deployment 🚀

### Heroku Deployment

1. **Fork/Clone this repository**
2. **Create a new Heroku app**
3. **Set environment variables:**
   ```env
   BOT_TOKEN=your_bot_token_here
   LOG_CHANNEL_ID=@your_log_channel
   APP_URL=https://your-app-name.herokuapp.com