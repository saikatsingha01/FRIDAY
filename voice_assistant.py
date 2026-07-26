from src.speech.speech_speaker import speak
import sounddevice as sd
from scipy.io.wavfile import write

from src.speech.speech_recognizer import transcribe
from src.core.command_handler import handle_command


SAMPLE_RATE = 16000
DURATION = 5


def record_audio():

    print("\nListening...")

    audio = sd.rec(
        int(SAMPLE_RATE * DURATION),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(
        "temp.wav",
        SAMPLE_RATE,
        audio
    )

    print("Recording finished.")



def clean_text(text):

    text = text.lower().strip()

    for symbol in [".", ",", "?", "!", "'"]:
        text = text.replace(symbol, "")

    return text



def should_shutdown(text):

    shutdown_words = [
        "exit",
        "shutdown",
        "shut down",
        "stop",
        "quit",
        "bye",
        "goodbye",
        "turn off"
    ]

    for word in shutdown_words:
        if word in text:
            return True

    return False



def main():

    print("Friday voice mode activated.")

    speak("Friday voice mode activated.")


    while True:

        record_audio()


        text = transcribe("temp.wav")


        text = clean_text(text)


        if not text:
            continue


        print("\nYou said:", text)


        if should_shutdown(text):

            response = "Shutting down."

            print("Friday:", response)

            speak(response)

            break



        response = handle_command(text)


        # Debugging response check
        print("DEBUG RESPONSE:", repr(response))


        if response:

            print("Friday:", response)

            speak(str(response))

        else:

            print("Friday did not generate a response.")



if __name__ == "__main__":

    main()