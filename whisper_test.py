from src.speech.speech_recognizer import transcribe
from src.core.brain import think


text = transcribe("temp.wav")

print("You said:", text)


result = think(text)


print("Friday:", result.get("response"))