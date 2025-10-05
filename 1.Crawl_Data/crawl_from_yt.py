from googleapiclient.discovery import build
import pandas as pd
import time

API_KEY = "AIzaSyBpwpNnGp7hTErrbzw7fXDaNAKyWM3IBps"
youtube = build('youtube', 'v3', developerKey=API_KEY)

query = "work life balance OR burnout OR stress kerja OR mental health"
search_response = youtube.search().list(
    q=query,
    part="id,snippet",
    maxResults=30,
    type="video",
    regionCode="ID"
).execute()

video_ids = [item['id']['videoId'] for item in search_response['items']]

comments = []

for vid in video_ids:
    print(f"Ambil komentar dari video: {vid}")
    next_page_token = None

    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=vid,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    "video_id": vid,
                    "author": comment['authorDisplayName'],
                    "text": comment['textDisplay'],
                    "likeCount": comment['likeCount'],
                    "publishedAt": comment['publishedAt']
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

            time.sleep(0.5)  # biar gak kena rate limit

        except Exception as e:
            print(f"⚠️ Lewati video {vid} karena error: {e}")
            break  # lanjut ke video berikutnya

df = pd.DataFrame(comments)
df.to_csv("youtube_comments_worklifebalance_full.csv", index=False)

print(f"✅ Total komentar disimpan: {len(df)}")
