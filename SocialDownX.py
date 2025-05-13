#!/usr/bin/env python3
import os
import sys
import re
import json
import time
import platform
import subprocess
import random
from datetime import datetime
from urllib.parse import urlparse
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, DownloadColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich import box
import shutil
import socket
import getpass

# Try to import optional dependencies
try:
    from rich import print
except ImportError:
    pass

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Constants
VERSION = "1.1"
DEVELOPER = "SocialDownX Team"
GITHUB_URL = "https://github.com/yourusername/SocialDownX"
CONTACT_EMAIL = "support@socialdownx.com"
HISTORY_FILE = "history.txt"
CONFIG_FILE = "config.json"
BRANDING_STRING = "SocialDownXAnmolKhadka"

# Detect platform
IS_ANDROID = "termux" in os.environ.get("PREFIX", "")
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

# Set download directory
if IS_ANDROID:
    DOWNLOAD_DIR = "/storage/emulated/0/Download/SocialDownX"
else:
    DOWNLOAD_DIR = os.path.expanduser("~/SocialDownX")

# Console setup
console = Console()

class SocialDownX:
    def __init__(self):
        self.check_dependencies()
        self.setup_directories()
        self.load_config()
        self.check_internet()
        
    def check_dependencies(self):
        """Check and install required dependencies"""
        required = ["yt-dlp", "requests", "rich"]
        missing = []
        
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append("yt-dlp")
        
        for package in required[1:]:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            console.print("[bold red]Missing dependencies detected![/bold red]")
            if self.confirm_action("Do you want to install missing dependencies?"):
                self.install_dependencies(missing)
    
    def install_dependencies(self, packages):
        """Install missing dependencies"""
        if "yt-dlp" in packages:
            try:
                console.print("[yellow]Installing yt-dlp...[/yellow]")
                subprocess.run(["pip", "install", "yt-dlp"], check=True)
                console.print("[green]yt-dlp installed successfully![/green]")
            except Exception as e:
                console.print(f"[red]Failed to install yt-dlp: {e}[/red]")
                sys.exit(1)
        
        if "requests" in packages or "rich" in packages:
            try:
                console.print("[yellow]Installing Python packages...[/yellow]")
                subprocess.run(["pip", "install"] + packages, check=True)
                console.print("[green]Packages installed successfully![/green]")
            except Exception as e:
                console.print(f"[red]Failed to install packages: {e}[/red]")
                sys.exit(1)
        
        if IS_ANDROID and not self.check_termux_api():
            console.print("[yellow]Termux API is not installed. Some features may not work.[/yellow]")
            if self.confirm_action("Do you want to install Termux API?"):
                subprocess.run(["pkg", "install", "-y", "termux-api"], check=True)
    
    def check_termux_api(self):
        """Check if Termux API is installed"""
        try:
            subprocess.run(["termux-notification", "--help"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def setup_directories(self):
        """Create necessary directories"""
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "w") as f:
                f.write("")
    
    def load_config(self):
        """Load or create config file"""
        self.config = {
            "default_quality": "best",
            "show_progress": True,
            "notifications": True,
            "clipboard_monitoring": False
        }
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    self.config.update(json.load(f))
            except json.JSONDecodeError:
                console.print("[red]Error reading config file. Using defaults.[/red]")
    
    def save_config(self):
        """Save config to file"""
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)
    
    def check_internet(self):
        """Check internet connection"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            self.internet_status = True
        except OSError:
            self.internet_status = False
    
    def show_splash(self):
        """Display splash screen"""
        splash = """
        ███████╗ ██████╗  ██████╗██╗ █████╗ ██╗     ██████╗ ███╗   ██╗██████╗ ██╗  ██╗
        ██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║    ██╔═══██╗████╗  ██║██╔══██╗╚██╗██╔╝
        ███████╗██║   ██║██║     ██║███████║██║    ██║   ██║██╔██╗ ██║██║  ██║ ╚███╔╝ 
        ╚════██║██║   ██║██║     ██║██╔══██║██║    ██║   ██║██║╚██╗██║██║  ██║ ██╔██╗ 
        ███████║╚██████╔╝╚██████╗██║██║  ██║██║    ╚██████╔╝██║ ╚████║██████╔╝██╔╝ ██╗
        ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝  ╚═╝╚═╝     ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝
        """
        console.print(Panel.fit(splash, style="bold blue"))
        console.print(f"[bold green]SocialDownX v{VERSION}[/bold green]")
        console.print(f"[italic]Developed by {DEVELOPER}[/italic]\n")
    
    def show_main_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.show_splash()
        
        # System info
        os_name = platform.system()
        if IS_ANDROID:
            os_name = "Android (Termux)"
        
        # Create info table
        info_table = Table.grid(padding=(0, 2))
        info_table.add_column(style="bold cyan")
        info_table.add_column()
        
        info_table.add_row("📱 OS:", os_name)
        info_table.add_row("👤 User:", getpass.getuser())
        info_table.add_row("📅 Date:", datetime.now().strftime("%Y-%m-%d"))
        info_table.add_row("⏰ Time:", datetime.now().strftime("%H:%M:%S"))
        info_table.add_row("📶 Internet:", "[green]✅ Connected[/green]" if self.internet_status else "[red]❌ Disconnected[/red]")
        
        console.print(Panel(info_table, title="System Info", border_style="blue"))
        
        # Main menu options
        menu = """
        [1] Download from URL
        [2] Batch download from file
        [3] View Download History
        [4] About the Creator
        [5] View Device Info
        [6] Exit
        """
        
        console.print(Panel.fit(menu, title="Main Menu", border_style="green"))
        
        choice = input("\nEnter your choice: ").strip()
        return choice
    
    def get_device_info(self):
        """Gather detailed device information"""
        info = {}
        
        # System info
        info["OS"] = platform.system()
        info["OS Version"] = platform.version()
        info["Hostname"] = platform.node()
        info["Architecture"] = platform.machine()
        info["Processor"] = platform.processor()
        
        if IS_ANDROID:
            try:
                # Try to get Android device info
                result = subprocess.run(["getprop", "ro.product.model"], capture_output=True, text=True)
                info["Device Model"] = result.stdout.strip()
                
                result = subprocess.run(["getprop", "ro.product.manufacturer"], capture_output=True, text=True)
                info["Manufacturer"] = result.stdout.strip()
                
                info["Platform"] = "Android (Termux)"
            except:
                info["Platform"] = "Android (Unknown Device)"
        
        # RAM info
        if HAS_PSUTIL:
            mem = psutil.virtual_memory()
            info["RAM"] = f"{mem.total / (1024**3):.1f}GB (Used: {mem.used / (1024**3):.1f}GB, {mem.percent}%)"
            
            # CPU info
            info["CPU Cores"] = psutil.cpu_count(logical=False)
            info["CPU Threads"] = psutil.cpu_count(logical=True)
            info["CPU Usage"] = f"{psutil.cpu_percent()}%"
            
            # Battery info
            try:
                battery = psutil.sensors_battery()
                if battery:
                    info["Battery"] = f"{battery.percent}%"
                    info["Power Plugged"] = "Yes" if battery.power_plugged else "No"
            except:
                pass
            
            # Disk info
            disk = psutil.disk_usage('/')
            info["Disk Total"] = f"{disk.total / (1024**3):.1f}GB"
            info["Disk Free"] = f"{disk.free / (1024**3):.1f}GB ({disk.percent}% used)"
        
        return info
    
    def display_device_info(self):
        """Show detailed device information"""
        info = self.get_device_info()
        
        table = Table(title="Device Information", box=box.ROUNDED)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in info.items():
            table.add_row(key, str(value))
        
        self.clear_screen()
        console.print(table)
        input("\nPress Enter to return to main menu...")
    
    def about_creator(self):
        """Display about/credits information"""
        about_text = f"""
        [bold]SocialDownX v{VERSION}[/bold]
        
        Developed by: [green]{DEVELOPER}[/green]
        GitHub: [blue]{GITHUB_URL}[/blue]
        Contact: [yellow]{CONTACT_EMAIL}[/yellow]
        
        [italic]A powerful tool to download videos and media from social platforms.[/italic]
        
        Features:
        - Supports multiple platforms (YouTube, Instagram, Twitter, etc.)
        - Batch downloads
        - Quality selection
        - Cross-platform compatibility
        - Beautiful terminal interface
        
        [bold yellow]Press 'S' three times quickly for an easter egg![/bold yellow]
        """
        
        self.clear_screen()
        console.print(Panel.fit(about_text, title="About SocialDownX"))
        
        # Easter egg check
        console.print("\nPress any key to continue...", end="")
        key_presses = []
        while True:
            try:
                key = input()
                if key.lower() == 's':
                    key_presses.append(key)
                    if len(key_presses) >= 3:
                        self.show_easter_egg()
                        break
                else:
                    break
            except:
                break
    
    def show_easter_egg(self):
        """Display a fun easter egg"""
        egg = """
        [bold blink]CONGRATULATIONS![/bold blink]
        
        You found the secret easter egg!
        
        [green]Here's a special message just for you:[/green]
        
        The answer to life, the universe, and everything is... [bold yellow]42[/bold yellow].
        
        [italic]Now go download some awesome videos![/italic]
        """
        
        self.clear_screen()
        console.print(Panel.fit(egg, style="bold magenta"))
        input("\nPress Enter to continue...")
    
    def download_from_url(self, url=None):
        """Download media from a single URL"""
        self.clear_screen()
        console.print(Panel.fit("Download from URL", style="bold blue"))
        
        if url is None:
            console.print("\nEnter the URL (or 'back' to return):")
            if HAS_PYPERCLIP and self.config["clipboard_monitoring"]:
                try:
                    clipboard = pyperclip.paste()
                    if self.is_valid_url(clipboard):
                        console.print(f"\nFound URL in clipboard: [blue]{clipboard}[/blue]")
                        if self.confirm_action("Use this URL?"):
                            url = clipboard
                except:
                    pass
            
            if url is None:
                url = input("URL: ").strip()
                if url.lower() == 'back':
                    return
        
        if not self.is_valid_url(url):
            console.print("[red]Invalid URL! Please enter a valid URL.[/red]")
            time.sleep(2)
            return self.download_from_url()
        
        platform_name = self.detect_platform(url)
        if not platform_name:
            console.print("[red]Unsupported platform![/red]")
            time.sleep(2)
            return
        
        # Get video info before downloading
        video_info = self.get_video_info(url)
        if not video_info:
            console.print("[red]Failed to get video information![/red]")
            time.sleep(2)
            return
        
        self.display_video_info(video_info)
        
        if not self.confirm_action("Proceed with download?"):
            return
        
        # Quality selection
        qualities = ["best", "1080p", "720p", "480p", "360p", "audio-only"]
        console.print("\nAvailable quality options:")
        for i, quality in enumerate(qualities, 1):
            console.print(f"[cyan][{i}][/cyan] {quality}")
        
        try:
            choice = int(input("\nSelect quality (default=1): ") or "1")
            quality = qualities[choice-1]
        except (ValueError, IndexError):
            quality = "best"
        
        # Download
        self.process_download(url, quality, video_info)
    
    def get_video_info(self, url):
        """Get detailed information about the video"""
        try:
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--no-playlist",
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None
            
            info = json.loads(result.stdout)
            
            # Extract relevant information
            video_info = {
                "title": info.get("title", "Unknown"),
                "uploader": info.get("uploader", "Unknown"),
                "duration": self.format_duration(info.get("duration", 0)),
                "formats": self.get_available_formats(info),
                "description": info.get("description", "No description available"),
                "thumbnail": info.get("thumbnail", ""),
                "filesize": self.format_size(info.get("filesize_approx", 0)),
                "platform": self.detect_platform(url)
            }
            
            return video_info
        except Exception as e:
            console.print(f"[red]Error getting video info: {e}[/red]")
            return None
    
    def get_available_formats(self, info):
        """Get available video formats"""
        formats = set()
        if "formats" in info:
            for fmt in info["formats"]:
                if "height" in fmt:
                    if fmt["height"]:
                        formats.add(f"{fmt['height']}p")
                elif "audio_only" in fmt and fmt["audio_only"]:
                    formats.add("audio-only")
        
        if not formats:
            if "height" in info:
                formats.add(f"{info['height']}p")
            else:
                formats.add("best")
        
        return sorted(formats, key=lambda x: int(x[:-1]) if x[:-1].isdigit() else 0, reverse=True)
    
    def format_duration(self, seconds):
        """Format duration in seconds to HH:MM:SS"""
        if not seconds:
            return "Unknown"
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    
    def format_size(self, bytes_size):
        """Format file size in bytes to human-readable format"""
        if not bytes_size:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f}{unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f}TB"
    
    def display_video_info(self, video_info):
        """Display video information in a formatted way"""
        self.clear_screen()
        
        info_table = Table.grid(padding=(0, 2))
        info_table.add_column(style="bold cyan")
        info_table.add_column()
        
        info_table.add_row("Title:", video_info["title"])
        info_table.add_row("Uploader:", video_info["uploader"])
        info_table.add_row("Duration:", video_info["duration"])
        info_table.add_row("Available Qualities:", ", ".join(video_info["formats"]))
        info_table.add_row("Description:", video_info["description"][:100] + "..." if len(video_info["description"]) > 100 else video_info["description"])
        info_table.add_row("Thumbnail:", video_info["thumbnail"])
        info_table.add_row("Estimated Size:", video_info["filesize"])
        info_table.add_row("Platform:", video_info["platform"])
        
        console.print(Panel(info_table, title="Video Information", border_style="blue"))
    
    def batch_download(self):
        """Download from multiple URLs in a file"""
        self.clear_screen()
        console.print(Panel.fit("Batch Download", style="bold blue"))
        
        console.print("\nEnter the path to the text file containing URLs (one per line):")
        console.print("(or 'back' to return)")
        file_path = input("File path: ").strip()
        
        if file_path.lower() == 'back':
            return
        
        if not os.path.exists(file_path):
            console.print("[red]File not found![/red]")
            time.sleep(2)
            return self.batch_download()
        
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        if not urls:
            console.print("[red]No valid URLs found in the file![/red]")
            time.sleep(2)
            return
        
        console.print(f"\nFound [green]{len(urls)}[/green] URLs in the file.")
        
        # Quality selection
        qualities = ["best", "1080p", "720p", "480p", "360p", "audio-only"]
        console.print("\nSelect quality for all downloads:")
        for i, quality in enumerate(qualities, 1):
            console.print(f"[cyan][{i}][/cyan] {quality}")
        
        try:
            choice = int(input("\nSelect quality (default=1): ") or "1")
            quality = qualities[choice-1]
        except (ValueError, IndexError):
            quality = "best"
        
        # Process each URL
        success = 0
        failed = 0
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing batch...", total=len(urls))
            
            for url in urls:
                progress.update(task, description=f"[cyan]Processing: {url[:50]}...")
                
                if self.is_valid_url(url):
                    video_info = self.get_video_info(url)
                    if video_info and self.process_download(url, quality, video_info, batch_mode=True):
                        success += 1
                    else:
                        failed += 1
                else:
                    failed += 1
                    self.log_to_history(f"Invalid URL skipped: {url}")
                
                progress.update(task, advance=1)
        
        console.print(f"\n[green]Batch complete![/green] Success: {success}, Failed: {failed}")
        input("\nPress Enter to continue...")
    
    def process_download(self, url, quality="best", video_info=None, batch_mode=False):
        """Process a single download"""
        try:
            # Get video info if not provided
            if video_info is None:
                video_info = self.get_video_info(url)
                if video_info is None:
                    return False
            
            # Create platform-specific directory
            platform_name = video_info["platform"]
            platform_dir = os.path.join(DOWNLOAD_DIR, platform_name)
            os.makedirs(platform_dir, exist_ok=True)
            
            # Format filename
            if platform_name.lower() == "youtube":
                filename_template = "%(title)s.%(ext)s"
            else:
                random_num = random.randint(10000, 99999)
                filename_template = f"%(title)s_{BRANDING_STRING}_{random_num}.%(ext)s"
            
            # yt-dlp command
            cmd = [
                "yt-dlp",
                "-f", self.get_quality_format(quality),
                "--no-playlist",
                "--merge-output-format", "mp4",
                "-o", os.path.join(platform_dir, filename_template),
                url
            ]
            
            if not batch_mode:
                self.clear_screen()
                console.print(f"\nDownloading from: [blue]{url}[/blue]")
                console.print(f"Quality: [green]{quality}[/green]")
                console.print(f"Saving to: [yellow]{platform_dir}[/yellow]")
                console.print(f"Filename format: [cyan]{filename_template.replace('%(title)s', video_info['title']).replace('%(ext)s', 'mp4')}[/cyan]\n")
            
            # Run with progress if not in batch mode
            if batch_mode:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    self.log_to_history(f"Downloaded: {url}")
                    return True
                else:
                    self.log_to_history(f"Failed: {url} - {result.stderr}")
                    return False
            else:
                with Progress(
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    "•",
                    DownloadColumn(),
                    "•",
                    TimeRemainingColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task("Downloading", total=100)
                    
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                    
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            # Simple progress parsing (yt-dlp progress is complex)
                            if "ETA" in output and "%" in output:
                                try:
                                    percent = float(output.split("%")[0].split()[-1])
                                    progress.update(task, completed=percent)
                                except:
                                    pass
                    
                    if process.returncode == 0:
                        console.print("[green]Download completed successfully![/green]")
                        self.log_to_history(f"Downloaded: {url}")
                        
                        # Trigger media scan on Android
                        if IS_ANDROID:
                            subprocess.run(["termux-media-scan", platform_dir])
                        
                        # Show notification
                        if self.config["notifications"]:
                            self.show_notification("Download Complete", f"Saved to {platform_dir}")
                        
                        return True
                    else:
                        console.print("[red]Download failed![/red]")
                        console.print(process.stderr.read())
                        self.log_to_history(f"Failed: {url}")
                        return False
        
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            self.log_to_history(f"Error: {url} - {str(e)}")
            return False
    
    def get_quality_format(self, quality):
        """Get yt-dlp format selector based on quality"""
        if quality == "audio-only":
            return "bestaudio"
        elif quality == "best":
            return "bestvideo+bestaudio"
        else:
            return f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]"
    
    def show_notification(self, title, message):
        """Show a system notification"""
        if IS_ANDROID:
            try:
                subprocess.run(["termux-notification", "--title", title, "--content", message])
            except:
                pass
        elif IS_LINUX:
            try:
                subprocess.run(["notify-send", title, message])
            except:
                pass
        elif IS_MACOS:
            try:
                subprocess.run(["osascript", "-e", f'display notification "{message}" with title "{title}"'])
            except:
                pass
        elif IS_WINDOWS:
            try:
                from win10toast import ToastNotifier
                ToastNotifier().show_toast(title, message)
            except:
                pass
    
    def view_download_history(self):
        """Display download history"""
        self.clear_screen()
        
        if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
            console.print("[yellow]No download history found.[/yellow]")
            input("\nPress Enter to continue...")
            return
        
        with open(HISTORY_FILE, "r") as f:
            history = f.readlines()
        
        table = Table(title="Download History", box=box.ROUNDED)
        table.add_column("Timestamp", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("URL", style="green")
        
        for entry in history[-50:]:  # Show last 50 entries
            parts = entry.strip().split(" - ", 2)
            if len(parts) >= 3:
                table.add_row(parts[0], parts[1], parts[2])
            elif len(parts) == 2:
                table.add_row(parts[0], "", parts[1])
            else:
                table.add_row("", "", parts[0])
        
        console.print(table)
        input("\nPress Enter to continue...")
    
    def log_to_history(self, message):
        """Log a message to history file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HISTORY_FILE, "a") as f:
            f.write(f"{timestamp} - {message}\n")
    
    def detect_platform(self, url):
        """Detect which platform the URL belongs to"""
        domain = urlparse(url).netloc.lower()
        
        if "youtube.com" in domain or "youtu.be" in domain:
            return "YouTube"
        elif "instagram.com" in domain:
            return "Instagram"
        elif "facebook.com" in domain or "fb.com" in domain:
            return "Facebook"
        elif "twitter.com" in domain or "x.com" in domain:
            return "Twitter"
        elif "tiktok.com" in domain:
            return "TikTok"
        elif "reddit.com" in domain:
            return "Reddit"
        elif "vimeo.com" in domain:
            return "Vimeo"
        elif "dailymotion.com" in domain:
            return "Dailymotion"
        elif "pinterest.com" in domain:
            return "Pinterest"
        elif "linkedin.com" in domain:
            return "LinkedIn"
        elif "threads.net" in domain:
            return "Threads"
        elif "snapchat.com" in domain:
            return "Snapchat"
        elif "tumblr.com" in domain:
            return "Tumblr"
        else:
            return None
    
    def is_valid_url(self, url):
        """Check if the URL is valid"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def confirm_action(self, message):
        """Ask for user confirmation"""
        console.print(f"\n{message} [Y/n]: ", end="")
        choice = input().strip().lower()
        return choice in ('', 'y', 'yes')
    
    def clear_screen(self):
        """Clear the terminal screen"""
        if IS_WINDOWS:
            os.system('cls')
        else:
            os.system('clear')
    
    def run(self):
        """Main application loop"""
        while True:
            choice = self.show_main_menu()
            
            if choice == "1":
                self.download_from_url()
            elif choice == "2":
                self.batch_download()
            elif choice == "3":
                self.view_download_history()
            elif choice == "4":
                self.about_creator()
            elif choice == "5":
                self.display_device_info()
            elif choice == "6":
                console.print("\n[bold green]Thank you for using SocialDownX![/bold green]")
                sys.exit(0)
            else:
                console.print("\n[red]Invalid choice! Please try again.[/red]")
                time.sleep(1)

if __name__ == "__main__":
    try:
        app = SocialDownX()
        app.run()
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user.[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]An error occurred: {e}[/red]")
        sys.exit(1)
