import os
import streamlit as st
import yt_dlp

def download_video(url):
    download_path = "./downloads"  # Use a local directory
    os.makedirs(download_path, exist_ok=True)  # Ensure the directory exists
    
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Save in downloads folder
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return download_path

# Streamlit UI
st.title("YouTube Video Downloader")
url = st.text_input("Enter YouTube Video URL")

if st.button("Download"):
    if url:
        st.write("Downloading...")
        try:
            save_path = download_video(url)
            st.success(f"Download completed! Video saved in {save_path}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
