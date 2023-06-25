import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import Controllers.TextController as TextController
# from GUI.Controllers import TextController
import cv2
import sys
sys.path.append('../SIGNiT')
import talTest
# from SIGNiT import talTest


action_frame = None
camera_label = None
globalRoot = None
cap = None
is_camera_running = False
frame = None
input_label = None
timer = 3
timer_selection = None
Signs_state = False 
text_layout = None
font = None

def init(root, close_window, navigate_to_main_screen):
    global action_frame, camera_label, globalRoot, input_label, timer_selection, text_layout, font
    globalRoot = root
    # Creating the action layout frame (initially hidden)
    action_frame = ttk.Frame(root)
    action_frame.pack(padx=20, pady=20)
    action_frame.pack_forget()

    # Creating the title label for the action screen
    action_title_label = ttk.Label(action_frame, text="SIGNiT", font=("Arial", 24))
    action_title_label.pack()
    
    signs = [
    {"name": "Space", "path": "GUI\\Images\\Special signs\\space.png"},
    {"name": "Comma", "path": "GUI\\Images\\Special signs\\comma.png"},
    {"name": "Delete", "path": "GUI\\Images\\Special signs\\delete.png"},
    {"name": "Dot", "path": "GUI\\Images\\Special signs\\dot.png"},
    {"name": "Question", "path": "GUI\\Images\\Special signs\\question.png"}
    ]

    specialSigns_frame = ttk.Frame(action_frame)
    specialSigns_frame.pack(padx=20, pady=20)

    for sign in signs:
        imgFrame = ttk.LabelFrame(specialSigns_frame, text=sign["name"])
        imgFrame.pack(side="right", padx=10, pady=10)
        img = ttk.Label(imgFrame)
        img.pack(side="right", padx=10, pady=10)

        # Loading and resizing the image
        image_path = sign["path"]
        photo = resizeImg(image_path)

        # Assigning the image to the label
        img.image = photo
        img.configure(image=photo)
        
    # Creating the buttons layout frame (for the action screen)
    buttons_frame = ttk.Frame(action_frame)
    buttons_frame.pack(side="top")

    # Creating the buttons on the action screen
    close_button = ttk.Button(buttons_frame, text="Close", command=close_window)
    close_button.pack(side="right", padx=10, pady=10)

    signs_map_button = ttk.Button(buttons_frame, text="Signs Map", command=open_signs_map) 
    signs_map_button.pack(side="right", padx=10, pady=10)

    stop_button = ttk.Button(buttons_frame, text="Stop", command=navigate_to_main_screen)
    stop_button.pack(side="right", padx=10, pady=10)

    # Create a Font object
    font = Font(family="Helvetica", size=10)

    
    # Creating the label to display the camera image
    cam_frame = ttk.Frame(action_frame)
    cam_frame.pack(side="left",padx=10, pady=10)

    input_frame = ttk.LabelFrame(cam_frame, text="Input")
    input_frame.pack(side='top', padx=10, pady=10)

    TextController.input_label = ttk.Label(input_frame, font = font ,text="Sample input")
    TextController.input_label.pack(side='left', expand=True, fill='both')
    # Creating the text field to show the user text
    text_frame = ttk.LabelFrame(cam_frame, text="Your text")
    text_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side="top")
    TextController.your_text_entry = ttk.Entry(text_frame, text="Sample text", font = font)
    TextController.your_text_entry.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    camera_label = ttk.Label(cam_frame)
    camera_label.pack(side="top",padx=10, pady=10)

    # Creating layout for textView
    text_layout = ttk.Frame(action_frame, width=5)
    text_layout.pack(side="right")
    # Creating the text field to show the user last input chars

    # Creating the buttons on the action screen
    clear_button = ttk.Button(input_frame, text="Clear input" ,command=TextController.clearInput)
    clear_button.pack(side="bottom", padx=10, pady=10)
    # Create a frame for the buttons
    settings_frame = ttk.Frame(text_layout, width=5)
    settings_frame.pack(side='right')
    # Creating timer for detecting signs
    timer_frame = ttk.LabelFrame(settings_frame, text="Timer (sec)")
    timer_frame.pack(side='top')
    timer_selection = tk.Spinbox(timer_frame, from_=2, to=10, width=5)
    timer_selection.pack(padx=10, pady=10)
    # Create a button that increases the font size when clicked
    fontSize_frame= ttk.LabelFrame(settings_frame, text="Font Size")
    fontSize_frame.pack(side='top')
    increase_button = ttk.Button(fontSize_frame, text="+", command=increase_font_size, width=5)
    increase_button.pack(side='top',padx=10, pady=10)
    # Create a button that decreases the font size when clicked
    decrease_button = ttk.Button(fontSize_frame, text="-", command=decrease_font_size, width=5)
    decrease_button.pack(side='top',padx=10, pady=10)

def increase_font_size():
    global font
    size = font['size']
    new_size = size + 2 if size < 32 else 32  # Reset to size 32 if it goes over
    font.configure(size=new_size)

def decrease_font_size():
    global font
    size = font['size']
    new_size = size - 2 if size > 8 else 8  # Reset to size 8 if it goes under
    font.configure(size=new_size)

def resizeImg(image_path, x=100, y=100):
    # Loading and resizing the image
    image = Image.open(image_path)
    image = image.resize((x, y))  # Adjust the size 
    return ImageTk.PhotoImage(image)
 
def pack():
    global action_frame
    action_frame.pack()

def setUpdateCallback(interval, callback):
    # The Callback function will be called every interval milliseconds to update the action frame view 
    global camera_label
    camera_label.after(interval, callback)

def start_camera(selected_com_port = "COM1"):
    global cap, is_camera_running, camera_label 
    # if selected_com_port == None:
    #     # selected_com_port = com_combobox.get()
    
    # Determine the camera index based on the selected COM port
    if selected_com_port == "COM1":
        camera_index = 0
    elif selected_com_port == "COM2":
        camera_index = 1
    elif selected_com_port == "COM3":
        camera_index = 2
    else:
        # Show error message and return False
        messagebox.showerror("Camera Error", "Invalid COM port selected")
        return False

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        # Show error message and return False
        messagebox.showerror("Camera Error", "Failed to open camera\nPlease choose another COM port")
        return False

    is_camera_running = True

    def update_image():
        global frame
        try:
            if is_camera_running:
                ret, frame = cap.read()
                talTest.detectSign(frame)
                if ret:
                    # Convert the OpenCV BGR image to PIL Image format
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(image)

                    # Resize the image to fit the layout
                    image = image.resize((400, 300))  # Adjust the size as per your requirement

                    # Convert the PIL Image to Tkinter PhotoImage format
                    photo = ImageTk.PhotoImage(image)

                    # Update the image label
                    camera_label.configure(image=photo)
                    camera_label.image = photo
        except Exception as e:
            print("ERROR: update_image()",e)
        finally:
        # Update the window every 10 milliseconds (adjust as per your requirement)
            detectSignThread()
            setUpdateCallback(10, update_image)
    update_image()
    return True

def detectSign():
    global frame, timer
    timer = int(timer_selection.get())
    TextController.detectedLetter = talTest.startTimer(timer) 
    TextController.handelInput(TextController.detectedLetter)

def detectSignThread():
    thread = threading.Thread(target=detectSign)
    thread.start()  

def stop_camera():
    global cap, is_camera_running
    if cap is not None:
        cap.release()
        cap = None
    is_camera_running = False

def hide():
    global action_frame
    action_frame.pack_forget()  # Hide the action frame

def open_signs_map():
    global action_frame, Signs_state, text_layout
    if not Signs_state:
        # Show Signs_frame
        Signs_frame = ttk.Frame(text_layout)
        Signs_frame.pack(side="right", padx=20, pady=20)
        imgFrame = ttk.LabelFrame(Signs_frame, text="Signs")
        imgFrame.pack(side="right", padx=10, pady=10)
        img = ttk.Label(imgFrame)
        img.pack(side="right", padx=10, pady=10)
        # Loading and resizing the image
        image_path = "GUI\\Images\\signs.png"
        photo = resizeImg(image_path, 500, 500)
        # Assigning the image to the label
        img.image = photo
        img.configure(image=photo)
        Signs_state = True

def apply_settings(settings_window, selected_com_port):
    stop_camera()
    if selected_com_port in ["COM1", "COM2", "COM3"]:
        if start_camera(selected_com_port):
            settings_window.destroy()
        else:
            messagebox.showerror("Camera Error", "Failed to open camera. Please choose another COM port.")
    else:
        messagebox.showerror("Camera Error", "Invalid COM port selected. Please choose a valid COM port.")
    settings_window.destroy()  # Close the settings window after applying settings