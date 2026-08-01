from src.speech.speech_recognizer import transcribe
from src.core.tool_router import handle_command


text = transcribe("temp.wav")

print("You said:", text)


response = handle_command(text)


print("Friday:", response)