from src.input.text_input import get_input
from src.core.command_handler import handle_command


def start_assistant():

    print("Friday is ready.")

    while True:

        command = get_input()

        response = handle_command(command)

        if response == "shutdown":
            print("Friday shutting down.")
            break

        print("Friday:", response)