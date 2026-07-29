from src.ai.providers.base_provider import BaseProvider
import ollama
import time


class OllamaProvider(BaseProvider):

    def __init__(self):
        self.model = "llama3.2:3b"


    def generate(self, prompt):

        try:
            print("\n--- LLM REQUEST START ---")

            print("Prompt length:", len(prompt), "characters")

            start_time = time.time()

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            end_time = time.time()

            print(
                "LLM generation time:",
                round(end_time - start_time, 2),
                "seconds"
            )

            print("--- LLM REQUEST END ---\n")


            return response["message"]["content"]


        except Exception as e:

            print("OLLAMA ERROR:", e)

            return None