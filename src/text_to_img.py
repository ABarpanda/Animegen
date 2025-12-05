from together import Together
import base64
import time
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
client = Together(api_key=TOGETHER_API_KEY)

def main(myprompt: str, img_file_name: str):
    """
    Generates an image from a prompt using the Together AI API and saves it to a file.

    Args:
        myprompt (str): The text prompt for scanning content.
        img_file_name (str): The base name for the output image file (without extension).
    """
    # Call the Together AI API to generate an image
    response = client.images.generate(
        prompt=myprompt,
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=1024,
        height=768,
        steps=1,
        n=1,
        response_format="b64_json", # Request the image as a Base64 encoded string
    )
    
    # Extract the Base64 string from the response
    imgstring: str = response.data[0].b64_json
    
    # Decode the Base64 string into binary image data
    imgdata: bytes = base64.b64decode(imgstring)
    
    # Construct the filename and save the binary data
    filename: str = f'{img_file_name}.png'
    with open(filename, 'wb') as f:
        f.write(imgdata)

if __name__=="__main__":
    main("Cat eating burger", "burger-cat")