import os
import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

def passFunction(value):
    pass
papyrus_file_name = 'edwin.jpg'
original_papyrus_img = cv.imread(filename=papyrus_file_name, flags=1)

dict_names = {0: 'Papyrus CV GUI',
              1: 'PAPYRUS_IMG',
              2: 'GRAY',
              3: 'TRACKER',
              4: 'HSV_TRACKER',
              }

papyrus_img_width = original_papyrus_img.shape[1]
papyrus_img_height = original_papyrus_img.shape[0]

resize_scale_factor = 1
new_img_width = int(papyrus_img_width / resize_scale_factor)
new_img_height = int(papyrus_img_height / resize_scale_factor)

img_resized = cv.resize(original_papyrus_img, 
                        dsize=(new_img_width, new_img_height))
flag = False
points = []
img = img_resized.copy()
p1 = (0, 0)
p3 = (img.shape[1], img.shape[0])
color = (0, 0 ,0)
HSV_pickup_val = 'IMAGE'
global HSV_outimg
def restore_img(*args):
    global HSV_outimg, cp, flag
    cp = img_resized
    HSV_outimg = img_resized
    update_img_helper(img_resized)
    crop_button.configure(state = ctk.NORMAL,)

def lock_img(img):
    update_img_helper(img)

def create_separator():
    separator = ttk.Separator(right_frame, orient='horizontal')
    separator.pack(fill='x', pady=5)

def transparent_rectangle(img, pt1, pt2, color, opacity):
    overlay = img.copy()
    output = img.copy()
    cv.rectangle(overlay, pt1, pt2, color, -1)
    cv.addWeighted(overlay, opacity, output, 1-opacity, 0, output)
    return output

def toggle_event_handling():
    global flag
    flag = not flag
    if flag:
        image_label.bind("<Button-1>", cropper_helper)
        image_label.bind("<Motion>", dynamic_rectangle)
        image_label.bind("<Button-3>", crop_event_tk)
        crop_button.configure(text="cropping",
                              fg_color="red",
                              )
    else:
        image_label.unbind("<Button-1>")
        image_label.unbind("<Motion>")
        image_label.unbind("<Button-3>")
        crop_button.configure(text="enter_crop_mode",
                              fg_color=['#2CC985', '#2FA572'],
                              )

cp = img_resized
HSV_outimg = img_resized
def cropper_helper(event):
    global flag, points, img, img_resized, p1, p3
    if not flag:
        return
    x, y = event.x, event.y
    cp = img_resized.copy()
    points.append((x,y))
    if len(points) == 2:
        (x1, y1), (x2, y2) = points
        p1 = (x1, y1)
        p3 = (x2, y2)
        cp = transparent_rectangle(cp, p1, p3, color, 0.5)
        points.clear()
    update_img_helper(cp)

def dynamic_rectangle(event):
    global flag, points, img, p1, p3
    if not flag or len(points) != 1:
        return
    x, y = event.x, event.y
    cp = img.copy()
    cp = transparent_rectangle(cp, points[0], (x,y), color, 0.3)
    update_img_helper(cp)

def crop_event_tk(event):
    global flag, img, img_resized, p1, p3, cropped_img, cp, HSV_outimg
    if len(points) == 0:
        (x1, y1), (x2, y2) = p1, p3
        cp = img_resized.copy()
        cp = cp[min(y1,y2):max(y1,y2), min(x1,x2):max(x1,x2)]
        update_img_helper(cp)
        flag = not flag
        crop_button.configure(text="enter_crop_mode",
                              fg_color=['#2CC985', '#2FA572'],
                              state = ctk.DISABLED,
                              )
        HSV_outimg = cp
        
def update_img_helper(img):
    img_pil = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    my_image = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
    image_label.configure(image=my_image)
    image_label.image = my_image

def update_image(value):
    blur_value = blur_scale.get()
    blurred_image = cv.GaussianBlur(img, (blur_value*2+1, blur_value*2+1), 0)
    update_img_helper(blurred_image)