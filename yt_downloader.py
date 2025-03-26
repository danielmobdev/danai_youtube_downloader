import streamlit as st
import yt_dlp
import os
import subprocess
import time

DOWNLOAD_PATH = "/Users/danielisaacithi/ai_agents/youtube_downloader"

def download_youtube_video(url, progress_bar):
    """Download YouTube video, remove metadata, and strip audio."""
    try:
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)

        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'format': 'bv*+ba/best[ext=mp4]',  # Best video+audio, prefer MP4
            'merge_output_format': 'mp4',
            'progress_hooks': [lambda d: update_progress(d, progress_bar)]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        # Ensure file is MP4
        if not file_path.endswith(".mp4"):
            file_path = file_path.replace(file_path.split('.')[-1], "mp4")

        # Remove metadata & audio
        clean_file_path = file_path.replace(".mp4", "_clean.mp4")
        subprocess.run([
            "ffmpeg", "-i", file_path, "-an", "-map", "0:v", "-c:v", "copy",
            "-metadata", "title=", "-metadata", "artist=", "-metadata", "album=",
            clean_file_path
        ], check=True)

        # Replace original file with cleaned version
        os.replace(clean_file_path, file_path)
        return file_path

    except Exception as e:
        return f"Error: {str(e)}"

def update_progress(d, progress_bar):
    """Update the progress bar in Streamlit."""
    if d['status'] == 'downloading':
        downloaded_bytes = d.get('downloaded_bytes', 0)
        total_bytes = d.get('total_bytes', 1)  # Avoid division by zero
        progress = downloaded_bytes / total_bytes
        progress_bar.progress(progress)

# 🎨 Streamlit UI
st.title("📹 YouTube Video Downloader (No Audio, No Metadata)")
url = st.text_input("Enter YouTube Video URL:")

if st.button("Download"):
    if url:
        st.write("⏳ Downloading... Please wait.")
        progress_bar = st.progress(0)  # Initialize progress bar
        time.sleep(1)  # Small delay for UI update

        file_path = download_youtube_video(url, progress_bar)
        
        if "Error" not in file_path:
            progress_bar.empty()  # Remove progress bar
            st.success("✅ Download Complete!")
            st.video(file_path)
            st.download_button("⬇ Download Video", open(file_path, "rb"), file_path.split("/")[-1])
        else:
            progress_bar.empty()
            st.error(file_path)
    else:
        st.warning("⚠️ Please enter a valid YouTube URL.")
