from google import genai
from dotenv import load_dotenv
import os
load_dotenv() # Load environment variables from .env file

class Brain:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("Jarv"))  # Use the API key from the environment variable

    def generate_content(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        return response.text
    def generate_image_imagen(self, prompt):
        # Use generate_image with the proper Imagen model and prompt kwarg
        response = self.client.models.generate_image(
            model="imagen-3.0-generate-002",
            prompt=prompt,
        )
        # Imagen returns a clean list of images directly
        for generated_image in response.generated_images:
            generated_image.image.save("generated_image.png")
        
