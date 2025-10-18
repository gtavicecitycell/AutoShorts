import os
import random
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import openai

# ===============================
# CONFIG - API KEYS from GitHub Secrets
# ===============================
openai.api_key = os.environ.get("OPENAI_API_KEY")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# ===============================
# STEP 1: Connect to YouTube
# ===============================
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
with open("client_secret.json", "w") as f:
    f.write(GOOGLE_CLIENT_SECRET)

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds = flow.run_console()  # First time: follow link, paste code
youtube = build("youtube", "v3", credentials=creds)

# ===============================
# STEP 2: Pick a topic
# ===============================
topics = ["AI Facts", "Space Mystery", "Motivational Quotes", "Life Hacks", "Health Tips"]
topic = random.choice(topics)

# ===============================
# STEP 3: Generate script using OpenAI
# ===============================
prompt = f"""
Write a 40-55 second YouTube Short script about "{topic}".
Start with a 1-line hook (5-8 words), then 3 short lines explaining the idea,
then a 1-line call-to-action "Follow for more!".
Make it high-energy and curiosity-driven.
"""
response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=150,
    temperature=0.8
)
script_text = response.choices[0].text.strip()
print("📝 Generated Script:\n", script_text)

# ===============================
# STEP 4: Create video (text on black background)
# ===============================
clip = TextClip(script_text, fontsize=50, color='white',
                size=(1080, 1920), bg_color='black',
                method='caption', align='center', duration=15)

clip.write_videofile("short.mp4", fps=24)

# ===============================
# STEP 5: Upload to YouTube
# ===============================
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": f"{topic} Shorts 🔥",
            "description": script_text,
            "tags": ["shorts", topic, "AI"],
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("short.mp4", resumable=True)
)
response = request.execute()
print("✅ Uploaded Video ID:", response["id"])
