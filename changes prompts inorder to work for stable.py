import requests
import json

class StabilityAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    def generate_image(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Fix: Ensure prompt is correctly formatted
        payload = {
            "prompt": prompt,  # Must be a plain string, not a list or object
            "cfg_scale": 7,
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 50
        }

        response = requests.post(self.api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
