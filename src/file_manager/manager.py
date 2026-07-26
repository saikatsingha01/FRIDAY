from pathlib import Path


OUTPUT_FILE = Path("output/message.txt")


def save_message(message):

    with open(OUTPUT_FILE, "w") as file:
        file.write(message)

    print("[FILE] Message saved.")