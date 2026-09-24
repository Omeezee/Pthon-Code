import os
import requests
import json
import time
from io import BytesIO
from PIL import Image

class SwarmAPI:
    def __init__(self, base_url="https://api.stability.ai/v2beta/stable-image/generate/core"):
       self.base_url = base_url
       self.session_id = None
        
        
class SwarmAPI:
    def __init__(self, api_key, base_url="https://api.stability.ai/v2beta/stable-image/generate/core"):
        self.base_url = base_url
        self.api_key = api_key

    def generate_image(self, prompt):
        # Ensure the prompt is not empty
        if not prompt:
            print("Prompt is empty.")
            return None

        # Prepare headers with API key
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "samples": 1,  # Number of images to generate
            "steps": 50,  # How many diffusion steps to take (higher values yield better results)
            "seed": None  # Optional seed for randomization (use None for random)
        }

        try:
            # Send POST request to the API
            response = requests.post(self.base_url, json=payload, headers=headers)
            data = response.json()

            # Check if the response contains image data
            if "image" in data:
                image_base64 = data["image"]
                return image_base64
            else:
                print(f"Error in response: {data}")
                return None

        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise
       

def get_new_session(self):
    response = requests.post(f"{self.base_url}/API/GetNewSession", json={})
    print("Raw Response:", response.text)  # Add this line to debug

    try:
        data = response.json()  # This is where the error occurs
    except Exception as e:
        print("JSON Decode Error:", e)
        return None
    return data

    def generate_image(self, prompt):
        # Get a new session if none exists
        if not self.session_id:
            self.get_new_session()

        payload = {
            "session_id": self.session_id,
            "images": 1,
            "prompt": prompt,
            "model": "sd3.5_medium/sd3.5_medium",
            "width": 1024,
            "height": 1024
        }

        try:
            response = requests.post(f"{self.base_url}/API/GenerateText2Image", json=payload)
            data = response.json()
            
            if "error_id" in data and data["error_id"] == "invalid_session_id":
                # Get a new session and retry
                self.get_new_session()
                payload["session_id"] = self.session_id
                response = requests.post(f"{self.base_url}/API/GenerateText2Image", json=payload)
                data = response.json()

            # Handle the image data
            if "images" in data:
                image_base64 = data["images"][0]
                return image_base64
            else:
                print(f"Error in response: {data}")
                return None

        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise

def process_text_prompts(filename):
    api = SwarmAPI()
    output_dir = "generated_images"
    os.makedirs(output_dir, exist_ok=True)

    with open(filename, 'r') as txtfile:
        for i, prompt in enumerate(txtfile):
            prompt = prompt.strip()
            if prompt:  # Skip empty lines
                try:
                    image_data = api.generate_image(prompt)
                    if image_data:
                        # Save image
                        image_path = os.path.join(output_dir, f"image_{i}.png")
                        image_bytes = BytesIO(base64.b64decode(image_data))
                        img = Image.open(image_bytes)
                        img.save(image_path, format='PNG')
                        print(f"Image saved at: {image_path}")
                    else:
                        print(f"No image generated for prompt: {prompt}")
                except Exception as e:
                    print(f"Error generating image for prompt: {prompt}")
                    print(f"Error: {str(e)}")
                time.sleep(1)  # Add delay between requests

if __name__ == "__main__":
    # Process prompts from a text file
    process_text_prompts(r"C:\Users\geode\Downloads\mass-create-stable-diffusion-images\scenic_prompts.txt")
