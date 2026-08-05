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

        self.providers       = {}
        self.active_provider = None

        self.register_default_providers()

    # ==========================================
    # PROVIDER REGISTRATION
    # ==========================================

    def register_default_providers(self):

        self.providers["ollama"] = OllamaProvider()
        self.active_provider     = "ollama"

    def register_provider(self, name, provider):

        self.providers[name] = provider

    # ==========================================
    # PROVIDER SWITCHING
    # ==========================================

    def set_provider(self, name):

        if name not in self.providers:
            raise ValueError(f"Unknown provider: {name}")

        self.active_provider = name

    def get_provider(self):

        return self.providers.get(self.active_provider)

    # ==========================================
    # GENERATION
    #
    # model param: optional override.
    # If None, the provider uses its current default.
    # If provided, the provider switches to that model
    # for this call only (not a permanent switch).
    #
    # num_predict param: optional max-token override for
    # this call only (used by the planner, whose complex
    # JSON responses exceed the default 2048 limit).
    #
    # format_json param: grammar-constrained JSON output for
    # this call only (used by the planner so llama3.2:3b
    # cannot stop mid-document). Off by default so natural
    # language generation stays untouched.
    # ==============================================

    def generate(self, prompt, model=None, num_predict=None, format_json=False):

        provider = self.get_provider()

        if provider is None:
            return None

        original_model = None
        original_predict = None

        if model and hasattr(provider, "set_model"):
            original_model = provider.get_model()
            provider.set_model(model)

        if num_predict and hasattr(provider, "num_predict"):
            original_predict = provider.num_predict
            provider.num_predict = num_predict

        try:
            response = provider.generate(prompt, format_json=format_json)
        finally:
            if original_model is not None:
                provider.set_model(original_model)
            if original_predict is not None:
                provider.num_predict = original_predict

        return response

    # ==========================================
    # INFORMATION
    # ==========================================

    def current_provider(self):
        return self.active_provider

    def available_providers(self):
        return list(self.providers.keys())


llm = LLMInterface()