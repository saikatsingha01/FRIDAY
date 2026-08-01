import json
import os
from datetime import datetime


HISTORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "memory_history.json"
)



# =====================================================
# LOAD / SAVE
# =====================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):

        return {
            "history": []
        }


    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def save_history(data):

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )



# =====================================================
# ADD HISTORY ENTRY
# =====================================================

def add_history(
    old_memory,
    new_memory
):

    history = load_history()


    entry = {

        "old_memory": old_memory,

        "new_memory": new_memory,

        "changed_at": datetime.now().isoformat()

    }


    history["history"].append(
        entry
    )


    save_history(
        history
    )


    return entry



# =====================================================
# READ HISTORY
# =====================================================

def get_history():

    return load_history()["history"]



def get_memory_history(keyword):

    history = load_history()["history"]


    results = []


    for item in history:


        old_text = item["old_memory"]["text"].lower()

        new_text = item["new_memory"]["text"].lower()



        if (

            keyword.lower() in old_text

            or

            keyword.lower() in new_text

        ):

            results.append(
                item
            )


    return results



def history_count():

    return len(
        load_history()["history"]
    )