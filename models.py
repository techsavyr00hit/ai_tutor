import requests

class ModelManager:
    def __init__(self):
        self.api_key = "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"
        self.model = "x-ai/grok-4-fast:free"
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def ask(self, prompt, context=""):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        user_message = prompt
        if context:
            user_message += "\n\nContext:\n" + context

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI tutor for high school math and science."},
                {"role": "user", "content": user_message}
            ]
        }
        try:
            response = requests.post(self.endpoint, headers=headers, json=data, timeout=20)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as e:
            return f"HTTP error: {e}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {e}"
        except KeyError:
            return "Unexpected response from OpenRouter AI."