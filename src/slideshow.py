import tkinter as tk
from PIL import Image, ImageTk
import json

# Load the image paths and associated texts from the JSON file
with open("story.json", 'r') as file:
    image_texts = json.load(file)

# Extract the image paths from the loaded JSON data
image_paths = list(image_texts.keys()) 

# Initialize the Tkinter root window
root = tk.Tk()
root.title("Image Slideshow with Text")

# Label to display the image
img_label = tk.Label(root)
img_label.pack()

# Label to display the text associated with the image
text_label = tk.Label(root, text="", font=("Arial", 14), wraplength=600)
text_label.pack(pady=10)

# Index to track the current image
idx = 0

# Pause flag to control the slideshow behavior
paused = False  

def update_image():
    """
    Updates the image and its associated text in the slideshow.
    
    This function will be called repeatedly to display the next image
    and associated text in the slideshow, with a 5-second interval.
    """
    global idx, paused
    
    # If the slideshow is paused, stop further updates
    if paused:
        return
    
    # Get the path and text of the current image
    img_path = image_paths[idx]
    text = image_texts[img_path]

    # Open the image, resize it, and convert it for Tkinter display
    img = Image.open(img_path)
    img = img.resize((600, 400))  # Resize image to fit the window
    img = ImageTk.PhotoImage(img)

    # Update the label with the new image
    img_label.config(image=img)
    img_label.image = img

    # Update the text label with the associated text
    text_label.config(text=text)

    # Increment the index, wrap around to the start if necessary
    idx = (idx + 1) % len(image_texts)

    # Schedule the next image update after 5000 ms (5 seconds)
    root.after(5000, update_image)  

def toggle_pause():
    """
    Toggles the paused state of the slideshow.
    
    If the slideshow is currently paused, it will resume. If it is playing,
    it will pause the slideshow.
    """
    global paused
    paused = not paused
    if not paused:
        update_image()  # Restart the slideshow if it was paused

def next_image():
    """
    Moves to the next image in the slideshow.
    """
    global idx
    idx = (idx + 1) % len(image_texts)  # Go to the next image, wrapping around if needed
    update_image()

def prev_image():
    """
    Moves to the previous image in the slideshow.
    """
    global idx
    idx = (idx - 1) % len(image_texts)  # Go to the previous image, wrapping around if needed
    update_image()

# Frame to hold the navigation buttons
btn_frame = tk.Frame(root)
btn_frame.pack()

# Button to go to the previous image
btn_prev = tk.Button(btn_frame, text="<< Previous", command=prev_image)
btn_prev.pack(side=tk.LEFT, padx=10)

# Button to pause/play the slideshow
btn_pause = tk.Button(btn_frame, text="⏸ Pause / ▶ Play", command=toggle_pause)
btn_pause.pack(side=tk.LEFT, padx=10)

# Button to go to the next image
btn_next = tk.Button(btn_frame, text="Next >>", command=next_image)
btn_next.pack(side=tk.LEFT, padx=10)

# Start the slideshow by updating the first image
update_image()

# Start the Tkinter event loop
root.mainloop()
