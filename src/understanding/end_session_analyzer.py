from src.ai.llm_interface import llm


# Leading conversation interjections a user pads a terse shutdown or
# dismissal with ("um, power down", "hmm, sleep"). The classifiers
# are conservative (YES-only); a padded interjection pushed the small
# model to "NO" and let a garbage canonical fact through. The strip
# is structural (a fixed leading-particle set) and never inspects the
# rest of the message, so it cannot change a statement's meaning.
_LEAD_INTERJECTIONS = (
    "um,", "umm,", "ummm,", "uh,", "hmm,", "hm,",
    "so,", "yeah,", "yep,", "okay,", "ok,", "k,",
    "oh,", "ah,", "well,", "anyway,",
)


def _strip_lead_interjections(user_message):
    """
    Removes a single leading interjection particle so a terse
    session-end or topic-dismissal phrase is classified on its own
    ("um, power down" -> "power down"). Returns the trimmed text.
    """
    text = (user_message or "").strip()
    lowered = text.lower()
    for prefix in _LEAD_INTERJECTIONS:
        if lowered.startswith(prefix):
            return text[len(prefix):].strip()
    return text


_TOPIC_DISMISSAL_PROMPT = (
    "You are classifying whether a user is telling the assistant to "
    "drop, skip, dismiss, or move on from the CURRENT topic or "
    "conversation (a meta-conversation instruction about the chat "
    "itself).\n\n"
    "Reply only YES or NO.\n\n"
    "YES examples:\n"
    "- \"dismiss this topic\" -> YES\n"
    "- \"miss this topic\" -> YES\n"
    "- \"skip this topic\" -> YES\n"
    "- \"move on\" -> YES\n"
    "- \"move on to the next topic\" -> YES\n"
    "- \"lets change the subject\" -> YES\n"
    "- \"never mind that\" -> YES\n"
    "- \"drop this topic\" -> YES\n"
    "- \"set that aside\" -> YES\n"
    "- \"set this aside\" -> YES\n"
    "- \"shelve this topic\" -> YES\n"
    "- \"shelve that\" -> YES\n\n"
    "NO examples (these are memory commands or normal statements, "
    "NOT topic dismissal):\n"
    "- \"forget my favorite food\" -> NO\n"
    "- \"forget my favorite food is lasagna\" -> NO\n"
    "- \"forget that I like coffee\" -> NO\n"
    "- \"remember my favorite food is sushi\" -> NO\n"
    "- \"my favorite food is lasagna\" -> NO\n"
    "- \"I have an RTX 4050\" -> NO\n"
    "- \"did you know I play Zelda\" -> NO\n"
    "- \"what was my favorite food before chicken curry\" -> NO\n"
    "- \"tell me a joke\" -> NO\n"
    "- \"hello\" -> NO\n"
    "- \"see you later\" -> NO\n"
    "- \"give me a summary\" -> NO\n"
    "- \"how are you\" -> NO\n"
    "- \"i am done for today\" -> NO\n\n"
    "User message: {msg}\n"
    "Answer (YES or NO):"
)


_PLANNING_PROMPT = (
    "You are classifying whether the user has stated a MULTI-STEP "
    "GOAL that the assistant should plan or help accomplish over "
    "several actions or steps — learning something new, building or "
    "creating something, organizing a schedule, or completing a "
    "project.\n\n"
    "Reply only YES or NO.\n\n"
    "YES examples (the user wants a plan or step-by-step help to "
    "achieve a larger goal):\n"
    "- \"i want to build a game\" -> YES\n"
    "- \"i want to learn python\" -> YES\n"
    "- \"study for exams\" -> YES\n"
    "- \"help me finish my project\" -> YES\n"
    "- \"make me a study schedule\" -> YES\n"
    "- \"i want to learn to play guitar\" -> YES\n"
    "- \"plan my week\" -> YES\n"
    "- \"help me get fit\" -> YES\n"
    "- \"i want to write a book\" -> YES\n"
    "- \"teach me how to code\" -> YES\n\n"
    "NO examples (single-step commands, memory statements, "
    "questions, or explanations — NOT a multi-step goal):\n"
    "- \"turn off the lights\" -> NO\n"
    "- \"play a song\" -> NO\n"
    "- \"set a timer\" -> NO\n"
    "- \"what is my favorite food\" -> NO\n"
    "- \"my favorite food is lasagna\" -> NO\n"
    "- \"remember my favorite food is sushi\" -> NO\n"
    "- \"forget my favorite food\" -> NO\n"
    "- \"what time is it\" -> NO\n"
    "- \"explain how electric cars work\" -> NO\n"
    "- \"tell me a joke\" -> NO\n"
    "- \"hello\" -> NO\n"
    "- \"see you later\" -> NO\n\n"
    "User message: {msg}\n"
    "Answer (YES or NO):"
)


_CLASSIFIER_PROMPT = (
    "You are classifying whether the user is ENDING THE SESSION "
    "or telling the assistant to go offline, sleep, rest, stop "
    "listening, or shut down.\n\n"
    "Reply only YES or NO.\n\n"
    "A standalone terse shutdown, sleep, or sign-off phrase — "
    "\"turn off\", \"power down\", \"sleep\", \"good night\", "
    "\"goodbye\", \"bye\", \"bye bye\", \"exit\", \"shut down\", "
    "\"done for today\" — with no target object and no other intent "
    "is YES.\n\n"
    "YES examples:\n"
    "- \"i am done for today\" -> YES\n"
    "- \"good night\" -> YES\n"
    "- \"time to sleep\" -> YES\n"
    "- \"i am going to rest\" -> YES\n"
    "- \"time to rest\" -> YES\n"
    "- \"going offline\" -> YES\n"
    "- \"shut down\" -> YES\n"
    "- \"turn off\" -> YES\n"
    "- \"power down\" -> YES\n"
    "- \"sleep\" -> YES\n"
    "- \"goodbye\" -> YES\n"
    "- \"bye\" -> YES\n"
    "- \"bye bye\" -> YES\n"
    "- \"i am going to sleep now\" -> YES\n"
    "- \"you can sleep now\" -> YES\n"
    "- \"lets call it a day\" -> YES\n"
    "- \"exit\" -> YES\n"
    "- \"this session is over\" -> YES\n"
    "- \"the session is over\" -> YES\n"
    "- \"session over\" -> YES\n\n"
    "NO examples (memory commands, questions, commands with a "
    "target object, or discussion — NOT session end):\n"
    "- \"forget my favorite food\" -> NO\n"
    "- \"forget the memory about my marathon\" -> NO\n"
    "- \"delete my best friend priya\" -> NO\n"
    "- \"remove my gym membership memory\" -> NO\n"
    "- \"erase my favorite food\" -> NO\n"
    "- \"turn off the music\" -> NO\n"
    "- \"shut down the pc\" -> NO\n"
    "- \"my favorite food is lasagna\" -> NO\n"
    "- \"this means this topic\" -> NO\n"
    "- \"explain this topic\" -> NO\n"
    "- \"what does this topic mean\" -> NO\n"
    "- \"we were working on the c program, right\" -> NO\n"
    "- \"what time is it\" -> NO\n"
    "- \"how are you\" -> NO\n"
    "- \"hello\" -> NO\n"
    "- \"see you later\" -> NO\n\n"
    "User message: {msg}\n"
    "Answer (YES or NO):"
)


def detect_end_session(user_message: str) -> bool:
    """
    Focused, conservative END_SESSION classifier for the
    Understanding Layer.

    The full understanding prompt is too large for the small model
    to follow the intent taxonomy reliably, so session-end detection
    gets a dedicated micro-prompt.

    Conservative by construction: only the exact 'YES' label
    is accepted. A false negative (a missed session end) is safe —
    the session simply continues and the honesty rules stop FRIDAY
    from claiming it went offline. A false positive would randomly
    stop the voice loop, so every other label is treated as "not a
    session end".
    """
    try:
        prompt = _CLASSIFIER_PROMPT.format(
            msg=_strip_lead_interjections(user_message)
        )
        response = llm.generate(prompt)
        label = (response or "").strip().lower()
        label = label.strip("\"'`.,;: ")
        return label == "yes"
    except Exception:
        return False


def detect_planning_request(user_message: str) -> bool:
    """
    Focused PLANNING-REQUEST classifier for the Understanding
    Layer.

    The full understanding prompt is too large for the small model
    to label goal-accomplishment requests reliably: "i want to
    build a game" / "i want to learn python" / "study for exams"
    come back as goal=remember_information with planning=False, so
    the plan never runs. A dedicated micro-prompt is the authority
    for whether the user stated a multi-step goal — the same
    precedent as end_session and topic-dismissal.

    Conservative by construction: only the exact 'YES' label is
    accepted. A false negative (a missed plan) is safe — the
    conversation simply proceeds without a plan. A false positive
    routes a single-step request through the planner, which answers
    it anyway, so the failure mode is a longer response, not a
    broken one.
    """
    try:
        prompt = _PLANNING_PROMPT.format(
            msg=_strip_lead_interjections(user_message)
        )
        response = llm.generate(prompt)
        label = (response or "").strip().lower()
        label = label.strip("\"'`.,;: ")
        return label == "yes"
    except Exception:
        return False


def detect_topic_dismissal(user_message: str) -> bool:
    """
    Focused, conservative TOPIC-DISMISSAL classifier for the
    Understanding Layer.

    Meta-discourse ("dismiss this topic", "miss this topic", "move
    on") is never a durable user fact, but the full understanding
    prompt lets the small model store a garbage canonical fact
    ("I miss this topic") for these messages. A dedicated
    micro-prompt decides whether the user is dismissing or moving
    on from the current topic/conversation.

    Conservative by construction: only the exact 'YES' label is
    accepted. Memory commands ("forget my favorite food") and
    normal statements are explicitly negative examples, so a false
    positive (which would suppress a legitimate memory write) is
    the one failure mode guarded against hardest.
    """
    try:
        prompt = _TOPIC_DISMISSAL_PROMPT.format(
            msg=_strip_lead_interjections(user_message)
        )
        response = llm.generate(prompt)
        label = (response or "").strip().lower()
        label = label.strip("\"'`.,;: ")
        return label == "yes"
    except Exception:
        return False
