
from ..config import settings
import requests

class HFModelClient:
    """Generic Hugging Face model wrapper."""

    def __init__(self, api_url: str | None = None, token: str | None = None):
        self.api_url = api_url or settings.HF_API_URL
        self.token = token or settings.HF_TOKEN
        if not self.token:
            raise RuntimeError("HUGGINGFACE_API_TOKEN not set")

    def generate(self, prompt: str, max_new_tokens: int = 512, temperature: float = 0.2) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "return_full_text": False,
            },
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.post(self.api_url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data and "generated_text" in data[0]:
            return data[0]["generated_text"]
        if isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        # Some HF backends return dict with 'error' or alternative shape; return as string
        return str(data)
