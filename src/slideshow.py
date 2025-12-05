import tkinter as tk
from PIL import Image, ImageTk
import json
from typing import List

with open("story.json", 'r') as file:
    image_texts = json.load(file)

# Iterate through keys to get image paths
image_paths: List[str] = list(image_texts.keys()) 

# Initialize the main window for the application
root = tk.Tk()
root.title("Image Slideshow with Text")

# Label widget to display the image
img_label = tk.Label(root)
img_label.pack()

# Label widget to display the text, with wrapping
text_label = tk.Label(root, text="", font=("Arial", 14), wraplength=600)
text_label.pack(pady=10)

idx: int = 0
paused: bool = False  

def update_image() -> None:
    """
    Updates the displayed image and text based on the current index.
    Schedules the next update unless paused.
    """
    global idx, paused
    # If paused, do not update the image
    if paused:
        return
    
    # Retrieve current image path and text
    img_path = image_paths[idx]
    text = image_texts[img_path]

    # Open and resize the image for display
    img = Image.open(img_path)
    img = img.resize((600, 400))  
    img = ImageTk.PhotoImage(img)

    # Update the labels
    img_label.config(image=img)
    img_label.image = img # Keep a reference to prevent garbage collection
    text_label.config(text=text)

    # Move to the next index (looping back to 0 if at end)
    idx = (idx + 1) % len(image_texts)
    
    # Schedule this function to run again after 5000ms (5 seconds)
    root.after(5000, update_image)  

def toggle_pause() -> None:
    """
    Toggles the pause state of the slideshow.
    """
    global paused
    paused = not paused
    # If unpausing, immediately update to resume the cycle
    if not paused:
        update_image()

def next_image() -> None:
    """
    advances to the next image in the slideshow.
    """
    global idx
    # Increment index with wrap-around
    idx = (idx + 1) % len(image_texts)
    update_image()

def prev_image() -> None:
    """
    Moves to the previous image in the slideshow.
    """
    global idx
    # Decrement index with wrap-around
    idx = (idx - 1) % len(image_texts)
    update_image()

# Frame to hold control buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

btn_prev = tk.Button(btn_frame, text="<< Previous", command=prev_image)
btn_prev.pack(side=tk.LEFT, padx=10)

btn_pause = tk.Button(btn_frame, text="⏸ Pause / ▶ Play", command=toggle_pause)
btn_pause.pack(side=tk.LEFT, padx=10)

btn_next = tk.Button(btn_frame, text="Next >>", command=next_image)
btn_next.pack(side=tk.LEFT, padx=10)

update_image()
root.mainloop()
