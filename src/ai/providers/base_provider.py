class BaseProvider:

    def generate(self, prompt):

        raise NotImplementedError(
            "Provider must implement generate()."
        )