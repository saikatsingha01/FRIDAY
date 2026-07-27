def find_relevant_context(message, context):

    if not context:
        return []


    message = message.lower()


    keywords = []


    for word in message.split():

        if len(word) > 3:
            keywords.append(word)



    relevant = []



    for item in context:

        previous_message = item["user"].lower()



        for keyword in keywords:

            if keyword in previous_message:

                relevant.append(item)

                break



    return relevant