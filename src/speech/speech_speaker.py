import pyttsx3


def speak(text):
    """
    Synthesize and play `text` through Windows SAPI5.

    A fresh pyttsx3 engine is created for every call.
    This is intentional: the Windows SAPI5 COM driver
    does not reliably resume audio synthesis on a
    persistent engine after the first runAndWait()
    drains the queue. Subsequent calls on the same
    engine instance are silently dropped by SAPI5
    even though no Python exception is raised and
    runAndWait() returns normally.

    Creating a new engine per utterance adds ~50-100 ms
    of COM initialisation overhead, which is imperceptible
    in normal voice assistant use.
    """
    print("TTS:", text)

    try:
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"TTS error: {e}")