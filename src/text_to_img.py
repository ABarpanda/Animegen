from together import Together
import base64
import time
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
TOGETHER_API_KEY = os.getenv("TOGETHER_AI_API_KEY")

# Initialize the Together API client with the provided API key
client = Together(api_key=TOGETHER_API_KEY)

def main(myprompt, img_file_name):
    """
    Generates an image using the Together API based on a text prompt and saves it as a PNG file.
    
    Args:
    - myprompt (str): The text prompt to generate the image.
    - img_file_name (str): The base name for the generated image file (without extension).
    
    This function generates the image, decodes the base64-encoded image data, 
    and saves it as a PNG file.
    """
    
    # Call Together API to generate an image based on the prompt
    response = client.images.generate(
        prompt=myprompt,  # The text prompt to generate the image
        model="black-forest-labs/FLUX.1-schnell-Free",  # Model used for image generation
        width=1024,  # Width of the generated image
        height=768,  # Height of the generated image
        steps=1,  # Number of steps for image generation
        n=1,  # Number of images to generate
        response_format="b64_json",  # The format of the response (base64 encoded image in JSON)
    )
  
    # Extract the base64-encoded image string from the response
    imgstring = response.data[0].b64_json
    
    # Decode the base64 string into image data
    imgdata = base64.b64decode(imgstring)
    
    # Define the file name with .png extension
    filename = f'{img_file_name}.png'
    
    # Write the decoded image data into a file
    with open(filename, 'wb') as f:
        f.write(imgdata)

if __name__=="__main__":
    # Generate an image based on the prompt "Cat eating burger" and save it with the name "burger-cat.png"
    main("Cat eating burger", "burger-cat")
