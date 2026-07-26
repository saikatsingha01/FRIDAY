import os


def load_skills():

    skills = {}

    skill_folder = os.path.dirname(__file__)

    for file in os.listdir(skill_folder):

        if file.endswith(".py") and file not in [
            "__init__.py",
            "skill_loader.py",
            "skill_registry.py"
        ]:

            skill_name = file.replace(".py", "")

            skills[skill_name] = skill_name


    return skills