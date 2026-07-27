import whisper
import torch


# Select GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Whisper running on: {device}")


# Load model
model = whisper.load_model(
    "small",
    device=device
)


def transcribe(audio_file):

    result = model.transcribe(
        audio_file,

        # Use GPU acceleration
        fp16=(device == "cuda"),

        # Help Whisper focus on English speech
        language="en",

        # Reduce random guesses
        temperature=0,

        # Better accuracy at the cost of a little speed
        beam_size=5
    )


    text = result["text"].strip().lower()


    print(
        "RAW WHISPER:",
        repr(text)
    )


    return text