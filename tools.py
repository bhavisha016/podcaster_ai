import os
import requests
from crewai_tools import SerperDevTool, FileWriterTool, FileReadTool
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

search_tool = SerperDevTool()
file_writer_tool = FileWriterTool()
file_read_tool = FileReadTool()

class GroqVoiceInput(BaseModel):
    script: str = Field(..., description="The podcast script text to convert to audio")
    output_path: str = Field(
        default="outputs/podcast-latest.wav",
        description="Where to save the audio file"
    )

class GroqVoiceTool(BaseTool):
    name: str = "Groq Voice Tool"
    description: str = (
        "Converts a podcast script into an audio file."
    )
    args_schema: type[BaseModel] = GroqVoiceInput

    def _run(self, script: str, output_path: str = "outputs/podcast-latest.wav") -> str:
        try:
            os.makedirs("outputs", exist_ok=True)

            url = "https://api.groq.com/openai/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "canopylabs/orpheus-v1-english",
                "input": script[:2000],
                "voice": "troy",
                "response_format": "wav"
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return f"Audio saved to {output_path}"
            else:
                return f"Voice generation failed: {response.text}"

        except Exception as e:
            return f"Voice generation failed: {str(e)}"

groq_voice_tool = GroqVoiceTool()