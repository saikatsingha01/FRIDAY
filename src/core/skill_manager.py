from src.skills.skill_registry import get_skill


def run_skill(command):
    """
    Executes a registered skill if one matches
    the user's command.

    Returns:
        Skill result (str/object) if handled.
        None if no skill matches.
    """

    if not command:
        return None

    command = command.strip()

    skill = get_skill(command)

    if skill is None:
        return None

    try:

        # Calculator skill
        if command.startswith("calculate"):

            expression = command.replace(
                "calculate",
                "",
                1
            ).strip()

            return skill(expression)

        # Generic skills
        return skill(command)

    except Exception as error:

        return (
            f"Skill execution failed: {error}"
        )