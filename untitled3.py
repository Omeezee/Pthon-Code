import os
import requests
import json
import time
import getpass
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# API Configuration
#STABILITY_KEY = getpass.getpass('sk-ejZ5pz0eBR2JWyu00HlqwwiWHh9sDESZTWLoAQe0nroqGfQZ')
#api_url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"
#headers = {
#    "Authorization": f"Bearer {STABILITY_KEY}"
#}
# API Configuration
STABILITY_KEY = getpass.getpass('sk-ejZ5pz0eBR2JWyu00HlqwwiWHh9sDESZTWLoAQe0nroqGfQZ')
api_url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

headers = {
    "Authorization": f"Bearer {STABILITY_KEY}"
}
# Load prompts from Excel
file_path = "C:/Users/geode/Downloads/AI_Image_Prompts.xlsx"  # Replace with your file path
df = pd.read_excel(file_path)
output_dir = "generated_images"
os.makedirs(output_dir, exist_ok=True)

# Function to send image generation request
def send_generation_request(prompt):
    params = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "samples": 1
    }

    print(f"Sending request for prompt: '{prompt}'")
    response = requests.post(api_url, headers=headers, json=params)

    if response.status_code == 200:
        try:
            image_data = response.json()["artifacts"][0]["base64"]
            return image_data
        except (KeyError, IndexError):
            print("Invalid response structure.")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Iterate through each column and prompt
for column_name in df.columns:
    print(f"Processing prompts from column: '{column_name}'")
    for i, prompt in enumerate(df[column_name].dropna()):  # Skip empty prompts
        image_data = send_generation_request(prompt)
        if image_data:
            # Decode and save the image
            image_path = os.path.join(output_dir, f"{column_name}_image_{i}.png")
            image_bytes = base64.b64decode(image_data)
            img = Image.open(BytesIO(image_bytes))
            img.save(image_path, format='PNG')
            print(f"Saved image to {image_path}")
        else:
            print(f"Failed to generate image for prompt: '{prompt}'")
