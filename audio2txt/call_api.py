#Import the openai Library
from openai import OpenAI

# Create an api client
client = OpenAI(api_key="sk-s8fXLRtRcSOHej4d0YB2rrfEQinRwTk8561FxdIAozBp6d5j")

# Load audio file
audio_file= open(r"D:\aData\SFT\视频转录0719\test4.mp4", "rb")

# Transcribe
transcription = client.audio.transcriptions.create(
  model="whisper-1",
  file=audio_file
)
# Print the transcribed text
print(transcription.text)