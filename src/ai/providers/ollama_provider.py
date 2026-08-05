import ollama


class OllamaProvider:
    """
    Ollama provider for FRIDAY.

    Capabilities:
    - Text generation (chat)
    - Embeddings (nomic-embed-text)
    - Temperature control
    - Health checks
    - Model switching
    """

    def __init__(self):

        self.model       = "llama3.2:3b"
        self.embed_model = "nomic-embed-text"

        # Deterministic output for understanding JSON.
        self.temperature = 0.0
        self.top_p       = 0.9
        self.num_predict = 2048

    # ==========================================
    # MODEL MANAGEMENT
    # ==========================================

    def set_model(self, model):
        self.model = model

    def get_model(self):
        return self.model

    # ==========================================
    # PARAMETERS
    # ==========================================

    def set_temperature(self, value):
        self.temperature = value

    def set_top_p(self, value):
        self.top_p = value

    def set_max_tokens(self, value):
        self.num_predict = max(512, value)

    # ==========================================
    # GENERATION
    # ==========================================

    def generate(self, prompt, format_json=False):

        try:

            request = dict(
                model=self.model,

                messages=[
                    {
                        "role":    "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature":    self.temperature,
                    "top_p":          self.top_p,
                    "num_predict":    self.num_predict,
                    "repeat_penalty": 1.1,
                }
            )

            # Grammar-constrained JSON output. Used by the planner,
            # whose long JSON responses llama3.2:3b otherwise stops
            # mid-document (truncated "steps": [ ...). The grammar
            # forces the decoder to complete a valid JSON document.
            if format_json:
                request["format"] = "json"

            response = ollama.chat(**request)

            return response["message"]["content"].strip()

        except Exception as error:

            print("OLLAMA ERROR:", error)

            return None

    # ==========================================
    # EMBEDDINGS
    # ==========================================

    def embed(self, text: str):
        """
        Returns a float vector for the given text.
        Uses nomic-embed-text — fast, single forward pass.
        Not generative. Does not call the chat model.
        """

        try:

            response = ollama.embeddings(
                model=self.embed_model,
                prompt=text,
            )

            return response["embedding"]

        except Exception as error:

            print("OLLAMA EMBED ERROR:", error)

            return None

    # ==========================================
    # HEALTH CHECK
    # ==========================================

    def is_available(self):

        try:
            ollama.list()
            return True
        except Exception:
            return False

    # ==========================================
    # INFORMATION
    # ==========================================

    def info(self):

        return {
            "provider":    "ollama",
            "model":       self.model,
            "embed_model": self.embed_model,
            "temperature": self.temperature,
            "top_p":       self.top_p,
            "max_tokens":  self.num_predict,
        }