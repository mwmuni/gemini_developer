import base64
from typing import Any, Generator, NoReturn
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
from vertexai.preview.generative_models import GenerationResponse
import vertexai.preview.generative_models as generative_models

class GeminiClient:
    
    def __init__(self) -> None:
        self.generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0,
        "top_p": 0.95,
        }

        self.safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_UNSPECIFIED: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
        
        self.chat_history = [
            {
                "parts": [
                    {
                        "text": '''You are a personal assistant. You can perform file operations, run code, and generate content.
                                You have access to standard unix commands and can run Python code.
                                Shell and python commands, should they have output, will be sent as the next message and be surrounded by <<<STDOUT BEGIN>>> and <<<STDOUT END>>>.
                                Your goal is to complete the task requested by the user to the best of your ability.
                                If there was no output from a series of shell commands, you will see a user response of "<<<STDOUT EMPTY>>>".
                                When running python or installing pip, prepend `hatch run` to the command.
                                Bash blocks must only contain a single command and have no prefix.
                                Python files must declare their filename as a comment in the first line of the file.
                                Ensure backtick characters are used to denote code blocks.
                                Use pdftotext to extract text from PDFs.
                                When using bash commands, always include the equivalent of `-y` for automatic yes to prompts.
                                '''
                    }
                ],
                "role": "user"
            },
            {
                "parts": [
                    {
                        "text": '''I will perform as you command.'''
                    }
                ],
                "role": "model"
            }
        ]
        
        servers = ["northamerica-northeast1 (Montréal)", "southamerica-east1 (São Paulo)", "us-central1 (Iowa)", "us-east1 (South Carolina)", "us-east4 (Northern Virginia)", "us-east5 (Columbus)", "us-south1 (Dallas)", "us-west1 (Oregon)", "us-west4 (Las Vegas)", "asia-east1 (Taiwan)", "asia-east2 (Hong Kong)", "asia-northeast1 (Tokyo)", "asia-northeast3 (Seoul)", "asia-south1 (Mumbai)", "asia-southeast1 (Singapore)", "australia-southeast1 (Sydney)", "europe-central2 (Warsaw)", "europe-north1 (Finland)", "europe-southwest1 (Madrid)", "europe-west1 (Belgium)", "europe-west2 (London)", "europe-west3 (Frankfurt)", "europe-west4 (Netherlands)", "europe-west6 (Zurich)", "europe-west8 (Milan)", "europe-west9 (Paris)", "me-central1 (Doha)", "me-central2 (Dammam)", "me-west1 (Tel Aviv)"]
        self.servers = [s.split(" ")[0] for s in servers]
        self.server_iter = self.get_server()
        
    # Define a yield statement to return the server and keep cycling through them
    def get_server(self) -> Generator[str, Any, NoReturn]:
        while True:
            for server in self.servers:
                yield server
        
    
    def generate(self, prompt: str | list = """Tell me a joke about a computer.""", role="user"):
        
        vertexai.init(project="gen-lang-client-0066875741", location=self.server_iter.__next__())
        model = GenerativeModel(
            "gemini-1.5-pro-001",
        )
        if isinstance(prompt, str):
            self.chat_history.append({"parts": [{"text": prompt}], "role": role})
        else:
            self.chat_history.append({"parts": [{"text": p} for p in prompt], "role": role})
        responses = model.generate_content(
            self.chat_history,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            stream=False,
        )

        # Check if the response is iterable
        if not isinstance(responses, GenerationResponse):
            # for response in responses:
            self.chat_history.append({"parts": [{"text": r} for r in responses], "role": "model"})
        else:
            self.chat_history.append({"parts": [{"text": responses.text}], "role": "model"})
        return responses


    

if __name__ == "__main__":
    gc = GeminiClient()
    gc.generate()

