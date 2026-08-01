from src.speech.speech_speaker import speak
from src.speech.speech_recognizer import transcribe
from src.speech.voice_detector import listen

from src.core.process import clean_text
from src.core.input_validator import validate_input
from src.core.conversation_manager import process_conversation
from src.core.context_manager import add_context


class VoiceAssistant:

    """
    Main runtime for FRIDAY.

    Responsibilities:
    - Listen
    - Transcribe
    - Validate
    - Process conversation
    - Speak response

    Future:
    - Wake word
    - Interrupt handling
    - Multi-modal input
    - Emotion detection
    - Streaming responses
    """


    SHUTDOWN_WORDS = [

        "exit",
        "shutdown",
        "shut down",
        "quit",
        "stop",
        "bye",
        "goodbye",
        "turn off"

    ]


    def should_shutdown(
        self,
        text
    ):

        text = text.lower()

        return any(

            word in text

            for word in self.SHUTDOWN_WORDS

        )


    def run(self):

        print(
            "Friday voice mode activated."
        )

        speak(
            "Friday voice mode activated."
        )


        while True:


            # ===================================
            # LISTEN
            # ===================================

            audio = listen()


            # ===================================
            # SPEECH TO TEXT
            # ===================================

            raw_text = transcribe(
                audio
            )


            print(
                "\nRAW:",
                repr(raw_text)
            )


            # ===================================
            # CLEAN INPUT
            # ===================================

            text = clean_text(
                raw_text
            )


            if not validate_input(
                text
            ):

                continue


            print(
                "\nUSER:",
                text
            )


            # ===================================
            # SHUTDOWN
            # ===================================

            if self.should_shutdown(
                text
            ):

                response = "Shutting down."


                print(
                    "\nFRIDAY:",
                    response
                )


                speak(
                    response
                )


                add_context(

                    text,

                    response

                )


                break



            # ===================================
            # COGNITIVE PIPELINE
            # ===================================

            result = process_conversation(
                text
            )


            # ===================================
            # RESPONSE EXTRACTION
            # ===================================

            if isinstance(
                result,
                dict
            ):

                response = result.get(

                    "response",

                    "I'm not sure how to respond."

                )

            else:

                response = (
                    "I'm not sure how to respond."
                )



            print(
                "\nFRIDAY:",
                response
            )


            speak(
                response
            )


            # ===================================
            # SHORT TERM CONTEXT
            # ===================================

            add_context(

                text,

                response

            )



def main():

    assistant = VoiceAssistant()

    assistant.run()



if __name__ == "__main__":

    main()