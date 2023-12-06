import csv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Set up YouTube Data API v3
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get playlist items or a single video
def get_video_list(input_id):
    if isinstance(input_id, list):
        # If input is a playlist (list of video IDs)
        videos = []
        for video_id in input_id:
            try:
                captions = YouTubeTranscriptApi.get_transcript(video_id)
                if captions:
                    videos.append({
                        'Video ID': video_id,
                        'Captions': captions
                    })
            except Exception as e:
                print(f"Error fetching captions for video {video_id}: {str(e)}")
        return videos
    else:
        # If input is a single video
        try:
            captions = YouTubeTranscriptApi.get_transcript(input_id)
            if captions:
                return [{
                    'Video ID': input_id,
                    'Captions': captions
                }]
        except Exception as e:
            print(f"Error fetching captions for video {input_id}: {str(e)}")
        return []

# Function to store captions in a CSV file
def store_captions_to_csv(video_list, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Video ID', 'Start', 'Duration', 'Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for video in video_list:
            video_id = video['Video ID']
            captions = video['Captions']
            for caption in captions:
                writer.writerow({
                    'Video ID': video_id,
                    'Start': caption['start'],
                    'Duration': caption['duration'],
                    'Text': caption['text']
                })

# Function to fetch captions for playlist or single video and store in CSV
def fetch_and_store_captions(video_ids, csv_filename):
    video_list = get_video_list(video_ids)
    store_captions_to_csv(video_list, csv_filename)

# Example usage:
# Replace 'YOUR_PLAYLIST_OR_VIDEO_ID' with the actual playlist ID or video ID
playlist_or_video_ids = ["O36lgfQ7mDk", "CcpmD5J8xOk", "k5S62lVAuy8", "DuSMAj0lGis"]

# Replace 'captions.csv' with your desired CSV filename
csv_filename = 'captions.csv'

fetch_and_store_captions(playlist_or_video_ids, csv_filename)
