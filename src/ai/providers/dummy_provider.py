from src.ai.providers.base_provider import BaseProvider


class DummyProvider(BaseProvider):

    def generate(self, prompt, format_json=False):

        # No AI yet.
        # Returning None tells the Brain
        # to continue with normal logic.

        return None