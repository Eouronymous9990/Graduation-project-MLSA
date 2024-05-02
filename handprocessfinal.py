#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from cvzone.HandTrackingModule import HandDetector
import os

# Initialize HandDetector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Function to apply filter based on hand gesture
def apply_filter(img, fingers):
    if fingers == [0, 1, 0, 0, 0]:
        return cv2.blur(img, (9, 9))  # Apply blur filter
    elif fingers == [0, 1, 1, 0, 0]:
        return cv2.GaussianBlur(img, (9, 9), 0)  # Apply Gaussian blur filter
    elif fingers == [1, 1, 1, 0, 0]:
        return cv2.medianBlur(img, 5)
    elif fingers == [0, 1, 1, 1, 1]:
        return cv2.bilateralFilter(img, 5, 75, 75)
    elif fingers == [0, 1, 1, 1, 0]:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif fingers == [0, 1, 1, 0, 1]:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        return img  # No filter applied

# Initialize Tkinter
root = tk.Toplevel()
root.title("Hand Gesture Filter")

# Create two frames for displaying webcam feed and filtered image
frame_webcam = tk.LabelFrame(root, text="Webcam Feed")
frame_webcam.pack(side="left", padx=10, pady=10)

frame_filtered = tk.LabelFrame(root, text="Filtered Image")
frame_filtered.pack(side="left", padx=10, pady=10)

# Create labels to display images
label_webcam = tk.Label(frame_webcam)
label_webcam.pack(padx=10, pady=10)

label_filtered = tk.Label(frame_filtered)
label_filtered.pack(padx=10, pady=10)

# Function to select an image file using file dialog
def browse_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])

# Create a button to browse for an image
browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack(pady=10)

image_path = None  # Variable to store the path of the selected image

# Function to update webcam feed and filtered image
def update_frames():
    ret, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if image_path is not None:
        selected_image = cv2.imread(image_path)
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            filtered_img = apply_filter(selected_image, fingers)
        else:
            filtered_img = selected_image
    else:
        filtered_img = img

    # Convert images to RGB format
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    filtered_img_rgb = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)

    # Convert images to PIL format
    img_pil = Image.fromarray(img_rgb)
    filtered_img_pil = Image.fromarray(filtered_img_rgb)

    # Convert images to PhotoImage format
    img_tk = ImageTk.PhotoImage(image=img_pil)
    filtered_img_tk = ImageTk.PhotoImage(image=filtered_img_pil)

    # Update labels with new images
    label_webcam.config(image=img_tk)
    label_webcam.image = img_tk

    label_filtered.config(image=filtered_img_tk)
    label_filtered.image = filtered_img_tk

    # Call update_frames function after 10ms
    label_webcam.after(10, update_frames)

# Initialize video capture from webcam
cap = cv2.VideoCapture(0)

# Call update_frames function to start displaying frames
update_frames()

# Run Tkinter main loop
root.mainloop()


# In[ ]:




