import os
import requests

def send_podcast_to_telegram(audio_path: str, caption: str = "🎙️ Your daily AI podcast is ready!"):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendAudio"
    with open(audio_path, "rb") as audio_file:
        response = requests.post(url, data={
            "chat_id": chat_id,
            "caption": caption,
            "title": "Daily AI Podcast",
            "performer": "PodcasterAI"
        }, files={"audio": audio_file})
    if response.status_code == 200:
        print("✅ Podcast sent to Telegram!")
    else:
        print(f"❌ Telegram send failed: {response.text}")