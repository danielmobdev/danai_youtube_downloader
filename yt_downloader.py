import os
import streamlit as st
import yt_dlp
import tempfile  # ✅ Use temporary directory

def download_video(url):
    # ✅ Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),  # Save inside temp dir
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)

    return video_filename  # Return path to the downloaded file

# Streamlit UI
st.title("YouTube Video Downloader")

url = st.text_input("Enter YouTube Video URL")
if st.button("Download"):
    if url:
        st.write("Downloading...")
        try:
            video_path = download_video(url)
            st.success(f"Download completed! Video saved at: {video_path}")

            # Provide download link in Streamlit
            with open(video_path, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=os.path.basename(video_path),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
