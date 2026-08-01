from src.ai.llm_interface import llm

from src.understanding.understanding_prompt import (
    build_understanding_prompt,
)

from src.understanding.understanding_parser import (
    parse_understanding,
)


class LLMUnderstanding:

    """
    Performs ONE LLM call for the complete
    Understanding Layer.

    Responsibilities:

    - Build the understanding prompt
    - Call the selected LLM
    - Parse the response

    Does NOT:

    - Validate
    - Perform reasoning
    - Retrieve memory
    - Build contracts
    """

    def understand(self, user_message: str):

        prompt = build_understanding_prompt(
            user_message
        )

        response = llm.generate(
            prompt
        )

        return parse_understanding(
            response
        )


llm_understanding = LLMUnderstanding()


def understand(user_message: str):

    return llm_understanding.understand(
        user_message
    )