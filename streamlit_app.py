import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the YouTube channel's videos page
url = "https://www.youtube.com/@LawSchoolToolbox/videos"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all video title elements
video_titles = soup.find_all('yt-formatted-string', {'id': 'video-title'})

# Extract the text from each title element
titles = [title.text.strip() for title in video_titles]

# Create a DataFrame with the titles
df = pd.DataFrame({'Video Titles': titles})

# Display the DataFrame as a table
print(df.to_string(index=False))

# Create a bar chart of the number of videos by first word
first_words = df['Video Titles'].str.split().str[0]
word_counts = first_words.value_counts().head(10)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
word_counts.plot(kind='bar')
plt.title('Top 10 First Words in Video Titles')
plt.xlabel('First Word')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
