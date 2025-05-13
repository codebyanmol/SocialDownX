🌀 SocialDownX
The Ultimate All-in-One Social Media Video & Post Downloader for Android (via Termux)

SocialDownX is a powerful and easy-to-use Python-based terminal tool designed to download videos and posts from all major social media platforms like Instagram, Facebook, Twitter (X), TikTok, Pinterest, Reddit, and even YouTube. Designed for Android users using Termux, this tool offers a fast, customizable, and feature-rich experience for your media collection needs.

✨ Features

🔗 All-in-One Social Media Downloader
Supports video and media downloads from platforms including:

Instagram (Reels, Posts, IGTV)

Facebook (Video, Post)

Twitter / X

TikTok (Watermark-free)

Pinterest

Reddit

YouTube (Videos, Playlists)

📂 Organized Media Storage

Downloads are saved to /sdcard/SocialDownX/PlatformName/

Each platform gets its own folder (e.g., /sdcard/SocialDownX/Instagram/)

Easily browsable in the gallery (visibility fixed automatically)

🧠 Smart File Naming (Except YouTube)

Filenames are appended with SocialDownXAnmolKhadka and a random number for uniqueness
Example: reel_SocialDownXAnmolKhadka_84217.mp4

🎥 Auto Video Metadata Display

Automatically shows detailed video info when you paste a link:

Title

Duration

Uploader

Description

Available qualities

File size

Thumbnail preview URL

📱 About Your Device

Device details shown in main menu:

Brand name

Processor name

CPU usage

RAM & RAM usage

Internal storage used/free

Battery level

🎛️ Download Options

Choose resolution (480p, 720p, 1080p, etc.)

Choose between video or audio download

MP3 support for music downloads (YouTube and TikTok)

🧠 Smart Queue System

Queue multiple URLs for batch downloads

Each URL is downloaded one by one with live status

⏳ Resume Support

Resume interrupted downloads where possible

🗓️ Schedule Downloads

Automatically schedule downloads at specific times

🎶 Download Subtitles

Download subtitles if available (YouTube, etc.)

Choose subtitle language

🔒 Login Support

Use your account credentials to download private/restricted videos
(Optional OAuth or username/password where required)

🌐 Proxy/VPN Support

Use HTTP/SOCKS proxies for geo-restricted content

🗃️ Playlist/Channel Downloads

Download entire YouTube playlists or all posts from a profile

📁 Auto File Compression (Optional)

Shrinks video size using ffmpeg with minimal quality loss

🎨 Cool Terminal UI

Uses rich library for colorful and animated output

Dark & light mode toggling

🔔 Notifications

Termux notification when a download completes

Optional sound/vibration

🗃️ Cloud Integration (Future Feature)

Upload completed downloads to Google Drive or Dropbox

📲 Android-Termux Compatible

100% tested on Android 11, 12, 13 with Termux

Fixes media not appearing in Gallery issue

💻 How to Install (Android-Termux)

Install Termux from F-Droid:
https://f-droid.org/packages/com.termux/

Update & Install dependencies:

bash
Copy
Edit
pkg update && pkg upgrade
pkg install python ffmpeg wget curl git
pip install yt-dlp rich psutil requests
termux-setup-storage
Clone this repo or copy the tool:

bash
Copy
Edit
git clone https://github.com/codebyanmol/SocialDownX.git
cd SocialDownX
Run the tool:

bash
Copy
Edit
python socialdownx.py
💾 Download Path

By default, all media will be downloaded to:

/sdcard/SocialDownX/PlatformName/

Media is saved with gallery visibility, so you can find your files easily in your file manager or gallery.

👨‍💻 Creator Info

Developer: Anmol Khadka 🇳🇵

GitHub: github.com/Anmol-Khadka

Project: SocialDownX – v1.0

Language: Python 3.11+

Interface: CLI (Terminal-based)

🧠 How It Works

Paste a video/post URL

Tool fetches info, shows preview

Choose format/quality

Download begins automatically

Files stored with smart names and visible in gallery

🛠️ Planned Features

GUI version with PyQt5 or TUI with curses

Telegram bot support

Discord bot version

Web dashboard with Flask

🔐 Disclaimer

This tool is meant for personal use only. Downloading copyrighted content from social media platforms without permission may violate their terms of service. The developer is not responsible for any misuse.

📬 Contribute

Pull requests, issues, and suggestions are welcome! Fork the repo and help make SocialDownX even better.
