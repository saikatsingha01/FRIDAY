from src.skills.calculator import calculate


skills = {
    "calculate": calculate
}


def get_skill(command):

    for trigger, skill in skills.items():

        if command.startswith(trigger):
            return skill

    return None