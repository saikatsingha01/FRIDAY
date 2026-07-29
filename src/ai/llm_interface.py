from src.ai.providers.ollama_provider import OllamaProvider


class LLMInterface:

    def __init__(self):

        self.provider = OllamaProvider()


    def set_provider(self, provider):

        self.provider = provider


    def generate(self, prompt):

        if self.provider is None:

            return None

        return self.provider.generate(prompt)


llm = LLMInterface()