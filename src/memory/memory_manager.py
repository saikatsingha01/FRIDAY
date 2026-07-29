import json
import os


from src.memory.memory_evaluator import evaluate_memory
from src.utils.logger import debug



MEMORY_FILE = os.path.join(

    os.path.dirname(__file__),

    "memory.json"

)



def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return {
            "memories":[]
        }


    with open(

        MEMORY_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)




def save_memory(data):

    with open(

        MEMORY_FILE,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            data,

            file,

            indent=4,

            ensure_ascii=False

        )




# ----------------------------------
# CATEGORY
# ----------------------------------


def detect_category(text):

    text=text.lower()



    if any(x in text for x in [

        "laptop",
        "pc",
        "computer",
        "gpu",
        "ram",
        "phone",
        "rtx"

    ]):

        return "device"



    if any(x in text for x in [

        "favorite",
        "like",
        "love",
        "hate",
        "prefer"

    ]):

        return "preference"



    if any(x in text for x in [

        "project",
        "building",
        "creating",
        "developing"

    ]):

        return "project"



    if any(x in text for x in [

        "my name",
        "i am",
        "i'm"

    ]):

        return "identity"



    return "general"




def importance(category):

    values={

        "identity":10,

        "project":9,

        "device":8,

        "preference":7,

        "general":3

    }


    return values.get(

        category,

        3

    )





# ----------------------------------
# SAVE MEMORY
# ----------------------------------


def auto_remember(fact):


    evaluation = evaluate_memory(fact)



    if not evaluation["should_remember"]:

        debug(
            "Memory rejected"
        )

        return False



    data=load_memory()



    for memory in data["memories"]:


        if memory["text"].lower()==fact.lower():

            return False



    ids=[

        m["id"]

        for m in data["memories"]

    ]


    new_id=max(ids,default=0)+1



    category=detect_category(fact)



    data["memories"].append({

        "id":new_id,

        "text":fact,

        "category":category,

        "importance":importance(category),

        "confidence":
        evaluation["confidence"]

    })


    save_memory(data)



    debug(
        f"Saved memory: {fact}"
    )


    return True





def remember(fact):

    if auto_remember(fact):

        return "I will remember that."

    return "I don't think this is important enough to remember."





# ----------------------------------
# READ
# ----------------------------------


def get_memory():

    return load_memory()



def get_all_memories():

    return load_memory()["memories"]



def memory_count():

    return len(
        load_memory()["memories"]
    )





# ----------------------------------
# DELETE
# ----------------------------------


def forget_memory(keyword):

    data=load_memory()



    old=len(data["memories"])



    data["memories"]=[

        m

        for m in data["memories"]

        if keyword.lower()
        not in m["text"].lower()

    ]



    save_memory(data)



    if len(data["memories"])<old:

        return "I forgot that."



    return "I couldn't find that memory."