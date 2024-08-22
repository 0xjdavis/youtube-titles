def get_youtube_videos(api_key, channel_id):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            order="date"
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
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()  # Return an empty dataframe if an error occurs
