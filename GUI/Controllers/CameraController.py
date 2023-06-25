import cv2
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from . import ActionFrame



cap = None
is_camera_running = False

def start_camera(selected_com_port = "COM1"):
    global cap, is_camera_running
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
        if is_camera_running:
            ret, frame = cap.read()
            if ret:
                # Convert the OpenCV BGR image to PIL Image format
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)

                # Resize the image to fit the layout
                image = image.resize((400, 300))  # Adjust the size as per your requirement

                # Convert the PIL Image to Tkinter PhotoImage format
                photo = ImageTk.PhotoImage(image)

                # Update the image label
                ActionFrame.camera_label.configure(image=photo)
                ActionFrame.camera_label.image = photo

            # Update the window every 10 milliseconds (adjust as per your requirement)
            ActionFrame.setUpdateCallback(10, update_image)

    update_image()
    return True