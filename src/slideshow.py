import tkinter as tk
from PIL import Image, ImageTk
import json
from typing import List

with open("story.json", 'r') as file:
    image_texts = json.load(file)

image_paths: List[str] = list(image_texts.keys()) 

root = tk.Tk()
root.title("Image Slideshow with Text")

img_label = tk.Label(root)
img_label.pack()

text_label = tk.Label(root, text="", font=("Arial", 14), wraplength=600)
text_label.pack(pady=10)

idx: int = 0
paused: bool = False  

def update_image() -> None:
    global idx, paused
    if paused:
        return
    
    img_path = image_paths[idx]
    text = image_texts[img_path]

    img = Image.open(img_path)
    img = img.resize((600, 400))  
    img = ImageTk.PhotoImage(img)

    img_label.config(image=img)
    img_label.image = img
    text_label.config(text=text)

    idx = (idx + 1) % len(image_texts)
    root.after(5000, update_image)  

def toggle_pause() -> None: # Commands for controlling the images
    global paused
    paused = not paused
    if not paused:
        update_image()

def next_image() -> None:
    global idx
    idx = (idx + 1) % len(image_texts)
    update_image()

def prev_image() -> None:
    global idx
    idx = (idx - 1) % len(image_texts)
    update_image()

btn_frame = tk.Frame(root) # Buttons for controlling the images through commands
btn_frame.pack()

btn_prev = tk.Button(btn_frame, text="<< Previous", command=prev_image)
btn_prev.pack(side=tk.LEFT, padx=10)

btn_pause = tk.Button(btn_frame, text="⏸ Pause / ▶ Play", command=toggle_pause)
btn_pause.pack(side=tk.LEFT, padx=10)

btn_next = tk.Button(btn_frame, text="Next >>", command=next_image)
btn_next.pack(side=tk.LEFT, padx=10)

update_image()
root.mainloop()
