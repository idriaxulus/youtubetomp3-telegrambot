from datetime import datetime

from yt_dlp import YoutubeDL


def get_video_title(url:str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title', 'Unknown Title')
    

def download_audio(url:str):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'downloads/track{timestamp}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"downloads/track{timestamp}.mp3"