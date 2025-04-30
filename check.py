import yt_dlp
import time
import os

def download_audio_from_youtube(url, output_path=None):
    if output_path is None:
        timestamp = int(time.time())
        filename_wo_ext = f"yt_audio_{timestamp}"
    else:
        filename_wo_ext = os.path.splitext(output_path)[0]

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename_wo_ext,  # Don't include .mp3 here
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    final_path = filename_wo_ext + '.mp3'
    return final_path
