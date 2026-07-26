from src.greeting import start
from src.utils.logger import log
from src.utils.config import load_settings
from src.file_manager.manager import save_message
from src.core.assistant import start_assistant


def main():

    settings = load_settings()

    if settings is None:
        return

    log("Application started")

    log(f"Assistant Name: {settings['assistant_name']}")
    log(f"Language: {settings['language']}")

    start()

    save_message("Project Friday started")

    start_assistant()

    log("Application finished")


if __name__ == "__main__":
    main()