import random

# Define lists of descriptive words and phrases
adjectives = [
    "breathtaking", "serene", "vibrant", "picturesque", "majestic", "enchanting",
    "idyllic", "stunning", "radiant", "glorious", "mystical", "ethereal", "captivating", "exquisite", "dreamlike"
]

scenic_features = [
    "Grand Canyon", "alpine lake", "tropical beach", "snow-capped mountain range",
    "lush forest", "rolling hills", "countryside valley", "crystal-clear river",
    "majestic waterfall", "coastal cliffs", "lavender fields", "desert oasis",
    "sunset over the sea", "arctic tundra", "vivid coral reef", "misty highlands",
    "sun-dappled meadow", "winding river", "ancient forest", "secluded cove"
]

details = [
    "at sunrise", "at sunset", "under a starry sky", "with a vibrant sky", "in the golden hour",
    "with dramatic clouds", "amidst a soft mist", "in autumn colors", "in spring bloom",
    "with sparkling water", "with deep blue reflections", "bathed in warm light", "with crisp air",
    "with a tranquil ambiance", "with a surreal atmosphere", "with brilliant hues", "with gentle fog",
    "in the soft glow of twilight", "with shimmering reflections", "with a clear, crisp sky"
]

styles = [
    "photorealistic", "watercolor", "oil painting", "digital art", "impressionistic",
    "vintage", "hyper-detailed", "3D render", "aerial view", "concept art",
    "cinematic", "vivid", "dreamy", "minimalist", "modern art"
]

# Set the number of prompts you want to generate
num_prompts = 1000

# Open (or create) the file in write mode
with open("scenic_prompts.txt", "w", encoding="utf-8") as f:
    for i in range(num_prompts):
        # Randomly select one element from each list
        adj = random.choice(adjectives)
        feature = random.choice(scenic_features)
        detail = random.choice(details)
        style = random.choice(styles)
        # Create the prompt sentence
        prompt = f"A {adj} view of {feature} {detail} in a {style} style."
        # Write the prompt as a new line in the file
        f.write(prompt + "\n")

print(f"Generated {num_prompts} scenic prompts in 'scenic_prompts.txt'.")

