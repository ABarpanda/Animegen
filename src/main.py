import timeit
import json
import os
import scene_split
import text_to_img
import shutil

# Start measuring the execution time
start = timeit.default_timer()

# Read the story from a text file
with open("story.txt", "r", encoding="utf-8") as f:
    story = f.read()

def clear_story_folder(folder_path="story"):
    """
    Clears the existing folder by deleting it and creating a new one.
    
    Args:
    - folder_path (str): The path to the folder to clear. Default is 'story'.
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Delete the existing folder
    os.makedirs(folder_path)  # Recreate the folder

# Clear the folder where images and other files will be stored
clear_story_folder()

# Split the story into scenes based on the provided similarity threshold
scenes = scene_split.main(story, 0.7)
print("Scenes splitted successfully!")

# Get the number of scenes generated
number_of_scenes = len(scenes)
print(f"Number of scenes: {number_of_scenes}")

print("\n")

# Prompt the user for the type of image they want to generate
image_type = input("Enter the type of image you want to generate (realistic, cartoon, abstract): ")
print("\n")

# Generate images for each scene using the specified image type
for i, scene in enumerate(scenes, 1):
    prompt = f"Make a {image_type} image of" + scene  # Create the prompt for the image generation
    text_to_img.main(prompt, f"story/image-{i}")  # Call the text-to-image function

# Prepare the data structure for storing the images and their corresponding prompts
story_dict = {f"story/image-{i}.png": line for i, line in enumerate(scenes, 1)}

# Save the data to a JSON file that contains the image paths and prompts
with open("story.json", "w") as f:
    json.dump(story_dict, f, indent=4)

# End the time measurement and calculate the execution time
end = timeit.default_timer()
print(f"Time taken: {end-start} seconds")

# Import the slideshow functionality (presumably, to show the generated images)
import slideshow
