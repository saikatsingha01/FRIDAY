import ollama


class OllamaProvider:
    """
    Ollama provider for FRIDAY.

    Future capabilities:
    - Multiple local models
    - Temperature control
    - Streaming
    - Vision models
    - Embedding models
    - Automatic retries
    - Health checks
    - Structured JSON mode
    """

    def __init__(self):

        self.model = "llama3.2:3b"

        # Deterministic output by default
        # Better for understanding JSON.
        self.temperature = 0.0

        self.top_p = 0.9

        # Increased to avoid truncated JSON
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

        # Prevent accidental tiny limits
        self.num_predict = max(512, value)

    # ==========================================
    # GENERATION
    # ==========================================

    def generate(self, prompt):

        try:

            response = ollama.chat(

                model=self.model,

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ],

                options={

                    "temperature": self.temperature,

                    "top_p": self.top_p,

                    "num_predict": self.num_predict,

                    "repeat_penalty": 1.1,

                }

            )

            return response["message"]["content"].strip()

        except Exception as error:

            print(

                "OLLAMA ERROR:",

                error

            )

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

            "provider": "ollama",

            "model": self.model,

            "temperature": self.temperature,

            "top_p": self.top_p,

            "max_tokens": self.num_predict

        }