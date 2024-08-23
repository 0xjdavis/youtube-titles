import streamlit as st
from googleapiclient.discovery import build
import pandas as pd

api_key=st.secrets["youtube_key"]

# Function to get videos from the YouTube channel
def get_youtube_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = None
    
    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,  # Maximum allowed value
            order="date",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            if item['id']['kind'] == "youtube#video":
                video_data = {
                    "Title": item['snippet']['title'],
                    "Published At": item['snippet']['publishedAt'],
                    "Video ID": item['id']['videoId']
                }
                videos.append(video_data)
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return pd.DataFrame(videos)

# Streamlit UI
st.title("YouTube Channel Video List")

api_key = st.text_input("YouTube API Key", type="password")
channel_id = st.text_input("YouTube Channel ID", value="UCLRAP5fUb-OpHEiTryypa0g")

if st.button
