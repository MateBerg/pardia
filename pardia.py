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
papyrus_file_name = 'greek_1.jpg'
original_papyrus_img = cv.imread(filename=papyrus_file_name, flags=1)

dict_names = {0: 'Papyrus CV GUI',
              1: 'PAPYRUS_IMG',
              2: 'GRAY',
              3: 'TRACKER',
              4: 'HSV_TRACKER',
              }

papyrus_img_width = original_papyrus_img.shape[1]
papyrus_img_height = original_papyrus_img.shape[0]

resize_scale_factor = 4
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

###########################################################################
###########################################################################

def show_splash_screen(duration_ms):
    splash_root = ctk.CTk()
    splash_root.overrideredirect(True)

    splash_image = cv.imread('mine_icon2.webp', flags=1)

    splash_img_width = splash_image.shape[1]
    splash_img_height = splash_image.shape[0]

    resize_scale_factor = 2
    new_img_width = int(splash_img_width / resize_scale_factor)
    new_img_height = int(splash_img_height / resize_scale_factor)

    splash_image = cv.resize(splash_image, 
                            dsize=(new_img_width, new_img_height))
    
    splash_img_pil = Image.fromarray(cv.cvtColor(splash_image, cv.COLOR_BGR2RGB))
    splash_my_image = ctk.CTkImage(light_image=splash_img_pil, 
                                   dark_image=splash_img_pil, 
                                   size=splash_img_pil.size)
    splash_image_label = ctk.CTkLabel(splash_root, image=splash_my_image, text="")
    splash_image_label.pack()

    # Center the splash screen on the screen
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    window_width = splash_image.shape[1]
    window_height = splash_image.shape[0]
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    splash_root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    # Show the splash screen for the specified duration then destroy
    splash_root.after(duration_ms, splash_root.destroy)
    splash_root.mainloop()

show_splash_screen(1000)

root = ctk.CTk()
root.iconbitmap('papyrus_icon.ico')
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("green")
root.title("PARDIA")

left_frame = ctk.CTkFrame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10)
right_frame = ctk.CTkFrame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10)

img_pil = Image.fromarray(cv.cvtColor(img_resized, cv.COLOR_BGR2RGB))
my_image = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
image_label = ctk.CTkLabel(left_frame, image=my_image, text="")
image_label.pack()

restore_button = ctk.CTkButton(master= right_frame,
                               text="restore_original_img",
                               corner_radius=5,
                               command=restore_img,
                           )
restore_button.pack(pady=5)

crop_button = ctk.CTkButton(master=right_frame,
                            text="enter_crop_mode",
                            command=toggle_event_handling,
                            corner_radius=5,
                            )
crop_button.pack(pady=5)

###########################################################################
###########################################################################

global LH, LS, LV, UH, US, UV
global LH_label, LS_label, LV_label
LH, LS, LV = 0, 0, 0
UH, US, UV = 255, 255, 255

def HSV_img_combolist(event=None):
    global LH, LS, LV, UH, US, UV
    hsv = cv.cvtColor(cp, cv.COLOR_BGR2HSV)
    LH = int(LH_slider.get())
    LS = int(LS_slider.get())
    LV = int(LV_slider.get())
    UH = int(UH_slider.get())
    US = int(US_slider.get())
    UV = int(UV_slider.get())
    
    LH_label.configure(text=f'LH: {LH}')
    UH_label.configure(text=f'UH: {UH}')
    LS_label.configure(text=f'LS: {LS}')
    US_label.configure(text=f'US: {US}')
    LV_label.configure(text=f'LV: {LV}')
    UV_label.configure(text=f'UV: {UV}')

    HSV_lower_bound = np.array([LH, LS, LV])
    HSV_upper_bound = np.array([UH, US, UV])

    HSV_mask = cv.inRange(hsv, HSV_lower_bound, HSV_upper_bound)
    HSV_result_by_mask = cv.bitwise_and(cp, cp, mask=HSV_mask)

    global HSV_pickup_val, HSV_outimg
    if HSV_pickup_val == 'IMAGE':
        update_img_helper(cp)
        HSV_outimg = cp
    elif HSV_pickup_val == 'BitwiseOR':
        update_img_helper(HSV_result_by_mask)
        HSV_outimg = HSV_result_by_mask
    else:
        update_img_helper(HSV_mask)
        HSV_outimg = HSV_mask
        HSV_mask = HSV_outimg

def update_HSV_pickup_val(event):
    global HSV_pickup_val
    HSV_pickup_val = HSV_pickup.get()
    HSV_img_combolist()

HSV_scales_frame = ctk.CTkFrame(right_frame)
HSV_scales_frame.pack(pady=10)

my_font = ctk.CTkFont(size=20, weight='bold')

HSV_label_title = ctk.CTkLabel(HSV_scales_frame,
                               text='HSV_detection',
                               text_color=['#2CC985', '#2FA572'],
                               font=my_font)
HSV_label_title.pack(side='top',pady=5)

HSV_pickup = ctk.CTkComboBox(HSV_scales_frame, 
                             values=['IMAGE' ,'BitwiseOR', 'MASK'],
                             state='readonly',
                             command=update_HSV_pickup_val
                             )
HSV_pickup.set('IMAGE')
HSV_pickup.pack(side='top')

def lower_HSV_slider(label, value, command):
    lower_attr = ctk.CTkSlider(HSV_scales_frame,
                               from_=0,
                               to=255,
                               orientation=ctk.HORIZONTAL,
                               command=command,
                               )
    lower_attr.set(0)
    lower_attr_label = ctk.CTkLabel(HSV_scales_frame,
                                    text=f'{label}: {value}')
    lower_attr_label.pack(side='top')
    lower_attr.pack(side='top')
    return lower_attr, lower_attr_label

def upper_HSV_slider(label, value, command):
    upper_attr = ctk.CTkSlider(HSV_scales_frame,
                            from_=0,
                            to=255,
                            orientation=ctk.HORIZONTAL,
                            command=command,
                            )
    upper_attr.set(255)
    upper_attr_label = ctk.CTkLabel(HSV_scales_frame,
                                    text=f'{label}: {value}')
    upper_attr_label.pack(side='top')
    upper_attr.pack(side='top')
    return upper_attr, upper_attr_label

LH_slider, LH_label = lower_HSV_slider('LH', LH, HSV_img_combolist)
UH_slider, UH_label = upper_HSV_slider('UH', UH, HSV_img_combolist)
LS_slider, LS_label = lower_HSV_slider('LS', LS, HSV_img_combolist)
US_slider, US_label = upper_HSV_slider('US', US, HSV_img_combolist)
LV_slider, LV_label = lower_HSV_slider('LV', LV, HSV_img_combolist)
UV_slider, UV_label = upper_HSV_slider('UV', UV, HSV_img_combolist)

###########################################################################
###########################################################################

morph_frame = ctk.CTkFrame(right_frame)
morph_frame.pack(pady=10)

morph_title = ctk.CTkLabel(morph_frame,
                               text='Morphological',
                               text_color=['#2CC985', '#2FA572'],
                               font=my_font)
morph_title.pack(side='top',pady=5)

global morph_done_val
morph_done_val = 0

def update_morph_done_val(event=None):
    global morph_done_val
    morph_done_val = morph_done.get()
    morph_combolist()

morph_done = ctk.CTkSwitch(morph_frame, text='done?', command=update_morph_done_val)
morph_done.deselect()
morph_done.pack(side='bottom', pady=5)

def morph_combolist(event=None):
    global ksize_val, iter_val, HSV_outimg, morph_done_val
    ksize_val = int(ksize_slider.get())*2+1 # to get only odd values
    iter_val = int(iter_slider.get())
    
    ksize_label.configure(text=f'ksize: {ksize_val}')
    iter_label.configure(text=f'iter: {iter_val}')

    ksize_tuple = np.ones((ksize_val, ksize_val), dtype=np.uint8)
    global morph_method_val, morph_outimg, HSV_outimg

    if morph_method_val == 'None':
        update_img_helper(HSV_outimg)

    elif morph_method_val == 'DILATION':
        dilation = cv.dilate(HSV_outimg.copy(), kernel=ksize_tuple, 
                             iterations=iter_val)
        update_img_helper(dilation)
    
    elif morph_method_val == 'EROSION':
        erosion = cv.erode(HSV_outimg.copy(), kernel=ksize_tuple, 
                             iterations=iter_val)
        update_img_helper(erosion)

    elif morph_method_val == 'OPENING':
        opening = cv.morphologyEx(HSV_outimg.copy(), cv.MORPH_OPEN, 
                                  kernel=ksize_tuple, 
                                  iterations=iter_val)
        update_img_helper(opening)

    elif morph_method_val == 'CLOSING':
        closing = cv.morphologyEx(HSV_outimg.copy(), cv.MORPH_CLOSE, 
                             kernel=ksize_tuple, 
                             iterations=iter_val)
        update_img_helper(closing)

def update_morph_method_val(event):
    global morph_method_val
    morph_method_val = morph_method_CB.get()
    morph_combolist()

morph_method_CB = ctk.CTkComboBox(morph_frame, 
                             values=['None', 'DILATION' ,'EROSION', 'OPENING', 'CLOSING'],
                             state='readonly',
                             command=update_morph_method_val
                             )
morph_method_CB.set('None')
morph_method_CB.pack(side='top')

def morph_slider(label, value, to_, command):
    morph_slider_val = ctk.CTkSlider(morph_frame,
                            from_=1,
                            to=to_,
                            orientation=ctk.HORIZONTAL,
                            command=command,
                            )
    morph_slider_val.set(1)
    morph_slider_val_label = ctk.CTkLabel(morph_frame,
                                    text=f'{label}: {value}')
    morph_slider_val_label.pack(side='top')
    morph_slider_val.pack(side='top')
    return morph_slider_val, morph_slider_val_label

ksize_slider, ksize_label = morph_slider('ksize', LH, 6,morph_combolist)
iter_slider, iter_label = morph_slider('iter', LH, 99, morph_combolist)

###########################################################################
###########################################################################

root.mainloop()