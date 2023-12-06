import csv
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

# Set up YouTube Data API v3
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get comments for a video
def get_video_comments(video_id):
    comments = []
    next_page_token = None

    while True:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,  # Adjust as needed
                pageToken=next_page_token
            ).execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            next_page_token = response.get('nextPageToken')

            if next_page_token is None:
                break

        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {str(e)}")
            break

    return comments

# Function to get video list with comments
def get_video_list_with_comments(video_ids):
    videos = []
    for video_id in video_ids:
        try:
            comments = get_video_comments(video_id)
            if comments:
                videos.append({
                    'Video ID': video_id,
                    'Comments': comments
                })
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {str(e)}")

    return videos

# Function to store comments in a CSV file
def store_comments_to_csv(video_list, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Video ID', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for video in video_list:
            video_id = video['Video ID']
            comments = video['Comments']
            writer.writerow({
                'Video ID': video_id,
                'Comments': '\n'.join(comments)
            })

# Function to fetch comments for video IDs and store in CSV
def fetch_and_store_comments(video_ids, csv_filename):
    video_list = get_video_list_with_comments(video_ids)
    store_comments_to_csv(video_list, csv_filename)

# Example usage:
video_ids = ["O36lgfQ7mDk", "CcpmD5J8xOk", "k5S62lVAuy8", "DuSMAj0lGis"]

# Replace 'comments.csv' with your desired CSV filename
csv_filename = 'comments.csv'

fetch_and_store_comments(video_ids, csv_filename)
