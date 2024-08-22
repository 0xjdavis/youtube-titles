import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re

# Function to extract Channel ID from URL
def extract_channel_id(url):
    # Regex pattern to match channel ID from URL
    match = re.search(r'(channel/|user/|@)([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(2)
    return None

# Function to get videos from the YouTube channel
api_key=st.secrets["youtube_key"]
def get_youtube_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,  # Adjust the number of videos retrieved
        order="date"  # Sort by publication date
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        if item['id']['kind'] == "youtube#video":
            video_data = {
                "Title": item['snippet']['title'],
                "Published At": item['snippet']['publishedAt'],
                "Video ID": item['id']['videoId']
            }
            videos.append(video_data)
    
    return pd.DataFrame(videos)

# Streamlit UI
st.title("YouTube Channel Video List")
st.write("Enter your YouTube API Key and Channel URL to get the video list.")

api_key = st.text_input("YouTube API Key", type="password")
channel_url = st.text_input("YouTube Channel URL", value="https://www.youtube.com/@LawSchoolToolbox")

if st.button("Get Videos"):
    if api_key and channel_url:
        channel_id = extract_channel_id(channel_url)
        if channel_id:
            videos_df = get_youtube_videos(api_key, channel_id)
            st.dataframe(videos_df)
            csv = videos_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="youtube_videos.csv",
                mime="text/csv",
            )
        else:
            st.error("Invalid YouTube Channel URL.")
    else:
        st.error("Please provide both API Key and Channel URL.")
