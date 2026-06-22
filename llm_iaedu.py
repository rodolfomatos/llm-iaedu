import json
import os
import sys
import uuid

import httpx

import llm
from llm import hookimpl


def _load_dotenv():
    local_path = os.path.join(os.getcwd(), ".env")
    if os.path.isfile(local_path):
        candidates = [local_path]
    else:
        candidates = [
            os.path.expanduser("~/.config/iaedu/env"),
            os.path.expanduser("~/.iaedu.env"),
        ]
    for dotenv_path in candidates:
        if not os.path.isfile(dotenv_path):
            continue
        with open(dotenv_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip()
                if key and val and key not in os.environ:
                    os.environ[key] = val


@hookimpl
def register_models(register):
    register(IaeduModel())


@hookimpl
def register_commands(cli):
    @cli.command(name="iaedu-configure")
    def iaedu_configure():
        """Configure iaedu.pt credentials interactively."""
        configure()


class IaeduModel(llm.Model):
    model_id = "iaedu"

    def execute(self, prompt, stream, response, conversation):
        _load_dotenv()
        api_key = os.environ.get("IAEDU_API_KEY") or llm.get_key("iaedu")
        channel_id = os.environ.get("IAEDU_CHANNEL_ID")
        endpoint = os.environ.get("IAEDU_ENDPOINT")
        agent_id = os.environ.get("IAEDU_AGENT_ID")

        if not api_key:
            raise RuntimeError(
                "IAEDU API key not set. Run 'llm iaedu-configure' to set up "
                "credentials, or set IAEDU_API_KEY in .env"
            )

        if not channel_id:
            raise ValueError(
                "IAEDU_CHANNEL_ID is required. " "Set it in .env or export it."
            )

        if not endpoint and not agent_id:
            raise ValueError("Either IAEDU_ENDPOINT or IAEDU_AGENT_ID must be set.")

        if endpoint and agent_id:
            raise ValueError(
                "Set only one of IAEDU_ENDPOINT or IAEDU_AGENT_ID, not both."
            )

        if endpoint:
            scheme, _, rest = endpoint.partition("://")
            if rest:
                while "//" in rest:
                    rest = rest.replace("//", "/")
                endpoint = f"{scheme}://{rest}"
        else:
            endpoint = f"https://api.iaedu.pt/agent-chat/api/v1/agent/{agent_id}/stream"

        # Stable thread_id per conversation for chat history
        thread_id = str(getattr(conversation, "id", uuid.uuid4()))

        # Build message from system prompt + user prompt
        text = prompt.prompt
        system = getattr(prompt, "system", None) or ""
        if system:
            text = f"{system}\n\n{text}"

        form_data = {
            "thread_id": (None, thread_id),
            "user_info": (None, "{}"),
            "channel_id": (None, channel_id),
            "message": (None, text),
        }

        headers = {"x-api-key": api_key}

        try:
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(
                    endpoint,
                    headers=headers,
                    files=form_data,
                    timeout=120.0,
                )
                resp.raise_for_status()

                seen_first_token = False
                for line in resp.iter_lines():
                    if not line:
                        continue
                    line = line.decode("utf-8") if isinstance(line, bytes) else line

                    data_str = line
                    if line.startswith("data: "):
                        data_str = line[6:].strip()

                    if data_str == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                    except json.JSONDecodeError:
                        if not line.startswith("data: "):
                            yield data_str
                        continue

                    evt_type = data.get("type", "")
                    if evt_type == "token":
                        content = data.get("content", "")
                        if content:
                            seen_first_token = True
                            yield content
                    elif evt_type == "message":
                        if seen_first_token:
                            continue
                        msg_content = data.get("content", {})
                        if isinstance(msg_content, dict):
                            text = msg_content.get("content", "")
                            if text:
                                yield text
                    elif evt_type == "done":
                        break
                    elif evt_type == "start":
                        continue
                    elif "choices" in data and len(data["choices"]) > 0:
                        delta = data["choices"][0].get("delta", {})
                        if "content" in delta:
                            yield delta["content"]
                    elif "content" in data:
                        yield data["content"]
                    elif "message" in data:
                        yield data["message"]
        except httpx.TimeoutException:
            raise RuntimeError("Request to iaedu.pt timed out after 120 seconds")
        except httpx.ConnectError as e:
            raise RuntimeError(
                f"Cannot connect to {endpoint}. Check your network and IAEDU_AGENT_ID."
            ) from e
        except OSError as e:
            raise RuntimeError(
                f"Network error connecting to {endpoint}: {e}"
            ) from e
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 401:
                raise RuntimeError(
                    "Authentication failed (401). Re-run 'llm iaedu-configure' with a fresh API key from iaedu.pt"
                ) from e
            if status == 404:
                raise RuntimeError(
                    "Agent not found (404). Check your IAEDU_AGENT_ID or IAEDU_ENDPOINT."
                ) from e
            raise RuntimeError(f"iaedu.pt API returned HTTP {status}") from e
        except httpx.StreamError as e:
            raise RuntimeError(f"Connection lost while streaming response: {e}") from e


def configure():
    config_dir = os.path.expanduser("~/.config/iaedu")
    config_file = os.path.join(config_dir, "env")

    print("============================================")
    print("  llm-iaedu — Interactive Setup")
    print("============================================")
    print()
    print("Go to iaedu.pt, open your agent, and copy the")
    print("three values it shows (Endpoint, API Key,")
    print("Channel ID). Paste them below.")
    print()

    endpoint = input("IAEDU Endpoint URL (paste from iaedu.pt): ").strip()
    while not endpoint:
        print("  Endpoint cannot be empty.")
        endpoint = input("IAEDU Endpoint URL: ").strip()

    api_key = input("IAEDU API Key (paste from iaedu.pt): ").strip()
    while not api_key:
        print("  API Key cannot be empty.")
        api_key = input("IAEDU API Key: ").strip()

    channel_id = input("IAEDU Channel ID (paste from iaedu.pt): ").strip()
    while not channel_id:
        print("  Channel ID cannot be empty.")
        channel_id = input("IAEDU Channel ID: ").strip()

    os.makedirs(config_dir, exist_ok=True)
    with open(config_file, "w") as f:
        f.write("# iaedu global config — used by llm-iaedu from any directory\n")
        f.write(f"IAEDU_ENDPOINT={endpoint}\n")
        f.write(f"IAEDU_CHANNEL_ID={channel_id}\n")
        f.write(f"IAEDU_API_KEY={api_key}\n")

    os.chmod(config_file, 0o600)
    print()
    print(f"  [OK] Config written to {config_file}")
    print()
    print("  You can now use: llm -m iaedu \"Your question\"")
    print()
    print("  Optional — make iaedu your default model:")
    print("    llm models default iaedu")
    print("  Then just: llm \"Your question\"")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "configure":
        configure()
    elif len(sys.argv) > 1 and sys.argv[1] == "start":
        print("Usage: llm -m iaedu \"Your question\"")
        print("  or:  llm iaedu-configure")
        print("  or:  llm models default iaedu")
    else:
        print("Usage: llm-iaedu configure")
        sys.exit(1)


if __name__ == "__main__":
    main()
