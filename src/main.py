import timeit
# Start the timer to measure the total execution time of the script
start = timeit.default_timer()
import json
import os
import scene_split
import text_to_img
import shutil

# Read the story content from a text file
with open("story.txt", "r", encoding="utf-8") as f:
    story = f.read()

def clear_story_folder(folder_path: str = "story") -> None:
    """
    Clears the specified folder if it exists, or creates it if it doesn't.

    Args:
        folder_path (str): The path to the folder. Defaults to "story".
    """
    # Check if the folder already exists
    if os.path.exists(folder_path):
        # Remove the folder and all its contents
        shutil.rmtree(folder_path)
    # Create a new, empty folder
    os.makedirs(folder_path)

# Prepare the output directory for images
clear_story_folder()

# Split the story into distinct scenes using semantic similarity
# The threshold 0.7 determines how similar sentences must be to remain in the same scene
scenes = scene_split.main(story,0.7)
print("Scenes splitted successfully!")

number_of_scenes = len(scenes)
print(f"Number of scenes: {number_of_scenes}")

print("\n")
# Prompt the user for the desired artistic style
image_type = input("Enter the type of image you want to generate (realistic, cartoon, abstract): ")
print("\n")

# Iterate through each scene to generate a corresponding image
for i, scene in enumerate(scenes, 1):
    # Construct the prompt for image generation, including the user's chosen style
    prompt = f"Make a {image_type} image of" + scene
    # Call the image generation function
    text_to_img.main(prompt, f"story/image-{i}")

# Create a dictionary mapping image filenames to their corresponding scene text
story_dict = {f"story/image-{i}.png": line for i, line in enumerate(scenes, 1)}

# Save the mapping to a JSON file for use in the slideshow
with open("story.json", "w") as f:
    json.dump(story_dict, f, indent=4)

# Stop the timer and print the total execution time
end = timeit.default_timer()
print(f"Time taken: {end-start} seconds")

import slideshow