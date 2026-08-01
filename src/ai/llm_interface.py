from src.ai.providers.ollama_provider import OllamaProvider


class LLMInterface:
    """
    Central interface for every language model.

    Brain should never directly communicate with
    Ollama or any future provider.

    Future providers:
    - OpenAI
    - Gemini
    - Claude
    - LM Studio
    - llama.cpp
    - AirLLM
    - Local GGUF
    """

    def __init__(self):

        self.providers = {}

        self.active_provider = None

        self.register_default_providers()



    # ==========================================
    # Provider Registration
    # ==========================================

    def register_default_providers(self):

        ollama = OllamaProvider()

        self.providers["ollama"] = ollama

        self.active_provider = "ollama"



    def register_provider(

        self,

        name,

        provider

    ):

        self.providers[name] = provider



    # ==========================================
    # Provider Switching
    # ==========================================

    def set_provider(

        self,

        name

    ):

        if name not in self.providers:

            raise ValueError(

                f"Unknown provider: {name}"

            )

        self.active_provider = name



    def get_provider(self):

        return self.providers.get(

            self.active_provider

        )



    # ==========================================
    # Generation
    # ==========================================

    def generate(

        self,

        prompt

    ):

        provider = self.get_provider()

        if provider is None:

            return None

        return provider.generate(

            prompt

        )



    # ==========================================
    # Information
    # ==========================================

    def current_provider(self):

        return self.active_provider



    def available_providers(self):

        return list(

            self.providers.keys()

        )



llm = LLMInterface()