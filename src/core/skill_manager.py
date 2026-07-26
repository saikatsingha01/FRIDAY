from src.skills.skill_registry import get_skill


def run_skill(command):

    skill = get_skill(command)

    if skill:

        if command.startswith("calculate"):

            expression = command.replace("calculate", "").strip()

            return skill(expression)

    return None