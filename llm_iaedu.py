import llm
from llm import hookimpl, NeedsKeyException
import os
import json
import uuid
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
        }
        
        # Get the prompt text (includes fragments and prompt string)
        text = prompt.prompt
        
        # Generate a unique thread ID for this request
        thread_id = str(uuid.uuid4())
        
        # Prepare form data (matching what the adapter expects to send to iaedu.pt)
        # Note: The adapter adds its own channel_id from its environment, so we don't send channel_id here.
        form_data = {
            'thread_id': (None, thread_id),
            'user_info': (None, '{}'),
            'message': (None, text)
        }
        
        # Make request to adapter (synchronous)
        with httpx.Client(timeout=60.0) as client:
            response_obj = client.post(
                f"{adapter_url}/v1/chat/completions",
                headers=headers,
                files=form_data,  # This will encode as multipart/form-data
                timeout=60.0
            )
            response_obj.raise_for_status()
            
            # Process the response line by line (SSE format)
            for line in response_obj.iter_lines():
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