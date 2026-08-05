from src.speech.speech_speaker import speak
from src.speech.speech_recognizer import transcribe
from src.speech.voice_detector import listen

from src.core.process import clean_text
from src.core.input_validator import validate_input
from src.core.conversation_manager import process_conversation
from src.core.context_manager import add_context, rollover

from src.utils.logger import logger


SHUTDOWN_WORDS = {
    "exit",
    "quit",
    "shutdown",
    "shut down",
    "turn off",
    "bye",
    "goodbye",
    "stop"
}


def should_shutdown(text):

    text = text.lower()

    return any(
        word in text
        for word in SHUTDOWN_WORDS
    )


def main():

    logger.info("Starting FRIDAY Voice")

    speak("Friday voice mode activated.")

    while True:

        audio_file = listen()

        raw_text = transcribe(audio_file)

        text = clean_text(raw_text)

        if not validate_input(text):
            logger.debug("Ignored invalid input")
            continue

        logger.user(text)

        if should_shutdown(text):

            response = "Shutting down."

            logger.friday(response)

            speak(response)

            add_context(
                text,
                response
            )

            # Issue 10: roll the session's working buffer into an
            # episode on shutdown so nothing is lost on exit.
            rollover(force=True)

            break

        result = process_conversation(text)

        response = result["response"]

        if not response:

            response = (
                "Sorry, I couldn't generate a response."
            )

        logger.friday(response)

        speak(response)

        add_context(
            text,
            response
        )

        # END_SESSION — the Understanding Layer classified a
        # natural-language session end ("you can sleep now", "go
        # to sleep", "shut down", ...) and the ExecutionManager
        # mapped it to a runtime signal. Roll the working buffer
        # into an episode and stop listening. No keyword lists.
        execution = result.get("execution")

        if (
            execution is not None
            and getattr(execution, "end_session", False)
        ):

            rollover(force=True)

            break

    logger.info("FRIDAY stopped")


if __name__ == "__main__":
    main()