#!/usr/bin/env python
import sys
import warnings
import os
import requests
from datetime import datetime
from src.podcaster.crew import Podcaster
from src.podcaster.delivery.telegram_bot import send_podcast_to_telegram
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def generate_audio(script_text, output_path="outputs/podcast-latest.wav"):
    url = "https://api.groq.com/openai/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }

    os.makedirs("outputs", exist_ok=True)

    payload = {
        "model": "canopylabs/orpheus-v1-english",
        "input": script_text[:800],   
        "voice": "troy",
        "response_format": "wav"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Audio saved to {output_path}")
        return output_path
    else:
        print(f"TTS failed: {response.text}")
        return None

def run():
    inputs = {
        'topic': 'AI LLMs',
        'current_month': str(datetime.now().month),
        'current_year': str(datetime.now().year)
    }
    try:
        Podcaster().crew().kickoff(inputs=inputs)

        script_files = [f for f in os.listdir("outputs") if f.startswith("script-")]
        if script_files:
            latest_script = sorted(script_files)[-1]
            with open(os.path.join("outputs", latest_script), "r") as f:
                script_text = f.read()

            audio_path = generate_audio(script_text)

            if audio_path and os.path.exists(audio_path):
                send_podcast_to_telegram(
                    audio_path,
                    caption=f"🎙️ Your daily AI podcast — {datetime.now().strftime('%B %d, %Y')}"
                )
            else:
                print("⚠️ Audio generation failed!")
        else:
            print("⚠️ No script file found!")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    inputs = {
        "topic": "AI LLMs",
        'current_month': str(datetime.now().month),
        'current_year': str(datetime.now().year)
    }
    try:
        Podcaster().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        Podcaster().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Podcaster().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()