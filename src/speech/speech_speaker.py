import pyttsx3


def speak(text):

    print("TTS:", text)

    engine = pyttsx3.init("sapi5")

    engine.setProperty(
        "rate",
        170
    )

    engine.say(text)

    engine.runAndWait()

    engine.stop()