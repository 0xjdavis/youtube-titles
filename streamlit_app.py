import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import os

# Set up YouTube API client
api_key = os.environ.get('youtube_key')
youtube = build('youtube', 'v3', developerKey=api_key)

def fetch_youtube_videos(channel_id):
    videos = []
    next_page_token = None
    
    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            order='date',
            type='video',
            pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response['items']:
            videos.append({
                'title': item['snippet']['title'],
                'video_id': item['id']['videoId'],
                'published_at': item['snippet']['publishedAt']
            })
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

# Streamlit app
st.title('Law School Toolbox YouTube Videos')

# Law School Toolbox channel ID
channel_id = 'UCnHBzCxvdkqGR_6iIJYD2Jw'

if api_key:
    videos = fetch_youtube_videos(channel_id)
    df = pd.DataFrame(videos)
    df['published_at'] = pd.to_datetime(df['published_at']).dt.date
    df = df.sort_values('published_at', ascending=False)
    
    st.write(f"Total videos: {len(df)}")
    
    # Display the table
    st.dataframe(df[['title', 'published_at']], width=800)
    
    # Add clickable links to the videos
    st.write("Click on a video title to watch:")
    for _, row in df.iterrows():
        st.write(f"[{row['title']}](https://www.youtube.com/watch?v={row['video_id']})")
else:
    st.error("YouTube API key not found. Please set the YOUTUBE_API_KEY environment variable.")
