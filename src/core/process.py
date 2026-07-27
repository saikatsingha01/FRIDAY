def clean_text(text):

    text = text.lower().strip()

    for symbol in [".", ",", "!", "'"]:
        text = text.replace(symbol, "")

    return text