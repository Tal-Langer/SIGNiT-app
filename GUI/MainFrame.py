import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import Controllers.TextController as TextController
# from GUI.Controllers import TextController



main_frame = None
com_combobox = None

# Creating the main layout frame
def init(root,open_action_screen):
    global main_frame, com_combobox
    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=20)

    # Creating the welcome label
    welcome_label = ttk.Label(main_frame, text="Welcome to SIGNiT", font=("Arial", 24))
    welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

    mainTxt_label = ttk.Label(main_frame, text="Real Time Translation of the Israeli Sign Language Letters into Text", font=("Arial", 16))
    mainTxt_label.grid(row=1, column=0, columnspan=2, pady=10)
    # Creating the image on the right side
    mainImage_label = ttk.Label(main_frame)
    mainImage_label.grid(row=2, column=1, padx=10, pady=10)

    # Loading and resizing the image
    mainImagePath = "GUI\\Images\\mainIMG.png" 
    photo = resizeImg(mainImagePath)

    # Assigning the image to the label
    mainImage_label.image = photo
    mainImage_label.configure(image=photo)


    # Creating the settings layout on the left side
    settings_frame = ttk.LabelFrame(main_frame, text="Settings")
    settings_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n")

    # Creating the combobox for available com ports
    com_label = ttk.Label(settings_frame, text="Camera COM Port:")
    com_label.grid(row=1, column=0, sticky="w")
    com_combobox = ttk.Combobox(settings_frame, values=["COM1", "COM2", "COM3"])  
    com_combobox.grid(row=1, column=1, padx=5, pady=10)

    # Creating the Start button
    style = ttk.Style()
    style.configure('Custom.TButton',background="green")
    start_button = ttk.Button(main_frame, text="Start", command=open_action_screen, style='Custom.TButton')
    start_button.grid(row=3, column=0, columnspan=2, pady=10)

def hide():
    global main_frame
    main_frame.pack_forget()

def pack():
    global main_frame
    main_frame.pack()

def resizeImg(image_path):
    # Loading and resizing the image
    image = Image.open(image_path)
    image = image.resize((400, 400))  # Adjust the size 
    return ImageTk.PhotoImage(image)
