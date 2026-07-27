from src.speech.speech_speaker import speak
from src.speech.speech_recognizer import transcribe
from src.speech.voice_detector import listen

from src.core.process import clean_text
from src.core.input_validator import validate_input
from src.core.conversation_manager import process_conversation
from src.core.context_manager import add_context



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


        # Voice activity detection
        audio_file = listen()



        # Speech to text
        raw_text = transcribe(audio_file)



        print(
            "RAW WHISPER:",
            repr(raw_text)
        )



        # Cleanup
        text = clean_text(raw_text)



        # Validation
        if not validate_input(text):

            print(
                "Input unclear, ignoring."
            )

            continue



        print(
            "\nYou said:",
            text
        )



        # Shutdown
        if should_shutdown(text):

            response = "Shutting down."


            print(
                "Friday:",
                response
            )


            speak(response)



            add_context(
                text,
                response
            )


            break




        # Conversation layer
        conversation_result = process_conversation(text)



        # Debug context reasoning
        print(
            "DEBUG CONTEXT:",
            conversation_result["context"]
        )



        response = conversation_result["response"]



        print(
            "DEBUG RESPONSE:",
            repr(response)
        )



        if response:


            print(
                "Friday:",
                response
            )


            speak(
                str(response)
            )



            # Save short-term context
            add_context(
                text,
                response
            )


        else:

            print(
                "Friday did not generate a response."
            )




if __name__ == "__main__":

    main()