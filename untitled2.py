import os
import requests
import json
import time
import getpass
import pandas as pd
from PIL import Image
from io import BytesIO

# API Configuration
STABILITY_KEY = getpass.getpass('sk-ejZ5pz0eBR2JWyu00HlqwwiWHh9sDESZTWLoAQe0nroqGfQZ')  # Prompt for API key
api_url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image"
headers = {
    "Authorization": f"Bearer {STABILITY_KEY}"
}

# Load prompts from Excel
df = pd.read_excel("C:/Users/geode/Downloads/AI_Image_Prompts.xlsx")  # Replace with your file path
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

    print(f"Sending request for prompt: {prompt}")
    response = requests.post(api_url, headers=headers, json=params)

    if response.status_code == 200:
        image_data = response.json()["artifacts"][0]["base64"]
        return image_data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Iterate through each column and prompt
for column_name in df.columns:
    print(f"Processing prompts from column: {column_name}")
    for i, prompt in enumerate(df[column_name].dropna()):  # Skip empty prompts
        image_data = send_generation_request(prompt)
        if image_data:
            # Save image from base64
            image_path = os.path.join(output_dir, f"{column_name}_image_{i}.png")
            with open(image_path, "wb") as img_file:
                img_file.write(BytesIO(base64.b64decode(image_data)).getbuffer())
            print(f"Saved image to {image_path}")
        else:
            print(f"Failed to generate image for prompt: {prompt}")
