import pyttsx3
import time

engine = pyttsx3.init()

engine.say("FIRST TEST")
engine.runAndWait()

time.sleep(1)

engine.say("SECOND TEST")
engine.runAndWait()

time.sleep(1)

engine.say("THIRD TEST")
engine.runAndWait()

time.sleep(1)

engine.say("FOURTH TEST")
engine.runAndWait()

time.sleep(1)

engine.say("FIFTH TEST")
engine.runAndWait()

print("All TTS calls completed.")