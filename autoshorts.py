import os, random, textwrap, requests
from moviepy.editor import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# 🔑 Connect to YouTube
scopes = ["https://www.googleapis.com/auth/youtube.upload"]
with open("client_secret.json", "w") as f:
    f.write(os.environ["GOOGLE_CLIENT_SECRET"])
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
creds = flow.run_console()
youtube = build("youtube", "v3", credentials=creds)

# 🧠 Pick a random trending topic
topics = ["AI Facts", "Space Mystery", "Motivational Quotes", "Life Hacks"]
topic = random.choice(topics)

# ✍️ Simple script generator
script = f"Here’s a {topic.lower()} you didn’t know! {topic} can change how we see the world."

# 🎨 Create short video (text on background)
clip = TextClip(script, fontsize=50, color='white', size=(1080,1920), bg_color='black', method='caption', align='center', duration=15)
clip.write_videofile("short.mp4", fps=24)

# 🎥 Upload to YouTube
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": f"{topic} Shorts 🔥",
            "description": script,
            "tags": ["shorts", topic],
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("short.mp4", resumable=True)
)
response = request.execute()
print("✅ Uploaded:", response["id"])
