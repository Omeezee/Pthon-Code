import os
import requests
import time
import json
from io import BytesIO
from PIL import Image
import base64

class StabilityAI:
    def __init__(self, api_key, base_url="https://api.stability.ai/v2beta/stable-image/generate/core"):
        self.base_url = base_url
        self.api_key = api_key

    def send_generation_request(self, params, files=None):
        """Sends an image generation request to Stability AI API."""
        headers = {
            "Accept": "image/*",  # Expect an image response
            "Authorization": f"Bearer {self.api_key}"
        }

        if files is None:
            files = {}

        # Send request
        print(f"Sending REST request to {self.base_url}...")
        response = requests.post(
            self.base_url,
            headers=headers,
            files=files,
        )

        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        return response

    def generate_image(self, prompt):
        if not prompt:
            print("Prompt is empty.")
            return None

        # Define request parameters
        params = {
            "text_prompts": prompt,
            "model": "stable-diffusion-xl",
            "width": "1024",
            "height": "1024",
            "samples": "1",
            "steps": "50",
            "cfg_scale": "7",
            "seed": ""  # Random seed
        }

        # Send request and handle response
        try:
            response = self.send_generation_request(params)
            
            if "image" in response.headers.get("Content-Type", ""):
                image_bytes = BytesIO(response.content)
                return image_bytes
            else:
                print(f"Unexpected response format: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

def process_text_prompts(filename, api_key):
    api = StabilityAI(api_key)
    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)

    with open(filename, 'r') as txtfile:
        for i, prompt in enumerate(txtfile):
            prompt = prompt.strip()
            if prompt:
                try:
                    image_bytes = api.generate_image(prompt)
                    if image_bytes:
                        image_path = os.path.join(output_dir, f"image_{i}.png")
                        img = Image.open(image_bytes)
                        img.save(image_path, format='PNG')
                        print(f"Image saved at: {image_path}")
                    else:
                        print(f"No image generated for prompt: {prompt}")
                except Exception as e:
                    print(f"Error generating image for prompt: {prompt}")
                    print(f"Error: {str(e)}")
                time.sleep(1)

if __name__ == "__main__":
    api_key = "sk-ZXW8pVNFPcWGo0I30A8NIrkK7eDhSzABVYKnxyhm3PvUFWJh"  # Replace with your actual API key
    if not api_key or api_key == "your_api_key_here":
        print("ERROR: Missing or invalid API key. Please enter a valid key.")
    else:
        process_text_prompts(r"C:\Users\geode\Downloads\mass-create-stable-diffusion-images\scenic_prompts.txt", api_key)
