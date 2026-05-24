import llm
from llm import hookimpl, NeedsKeyException
import os
import json
import httpx

@hookimpl
def register_models(register):
    register(IaeduModel())

class IaeduModel(llm.Model):
    model_id = "iaedu"
    # This model supports streaming by returning a generator
    # The llm framework will handle streaming appropriately

    def execute(self, prompt, stream, response, conversation):
        # Get API key using llm's key system
        key = llm.get_key("iaedu")
        if not key:
            raise NeedsKeyException(
                "IAEDU API key not set. Use 'llm keys set iaedu' to set it."
            )
        
        # Get adapter URL from environment or default to localhost:4000
        adapter_url = os.getenv("IAEDU_ENDPOINT", "http://localhost:4000")
        
        # Prepare headers
        headers = {
            "x-api-key": key,
            "Content-Type": "application/json"
        }
        
        # Get the prompt text (includes fragments and prompt string)
        text = prompt.prompt
        
        # Prepare request body in OpenAI format with a single user message
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],
            "model": self.model_id,  # Adapter ignores this but we send it anyway
        }
        
        # Add non-None options from prompt.options
        if prompt.options:
            options_dict = prompt.options.dict()
            # Filter out None values
            options_dict = {k: v for k, v in options_dict.items() if v is not None}
            data.update(options_dict)
        
        # Make request to adapter (synchronous)
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{adapter_url}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            
            # Process the response line by line (SSE format)
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8') if isinstance(line, bytes) else line
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except (json.JSONDecodeError, KeyError):
                            # Ignore malformed lines
                            pass