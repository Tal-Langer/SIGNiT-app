import traceback

try:
    import tkinter as tk
    import MainFrame, ActionFrame
    # from GUI import MainFrame, ActionFrame

    def close_window():
        ActionFrame.stop_camera()
        root.destroy()

    def navigate_to_main_screen():
        ActionFrame.stop_camera()
        ActionFrame.hide() # Hide the action frame
        MainFrame.pack()  # Show the main frame

    def open_action_screen():
        # Check if the camera is successfully opened
        if not ActionFrame.start_camera():
            # Return to the main screen if camera opening failed
            return
        # Hide the main frame
        MainFrame.hide()
        # Show the action frame
        ActionFrame.pack()

    root = tk.Tk()
    root.title("SIGNiT")
    # Create and show Main screen
    MainFrame.init(root, open_action_screen)
    ActionFrame.init(root, close_window, navigate_to_main_screen)
    root.mainloop()
except Exception as e:
    with open('log.txt', 'w') as f:
        f.write(traceback.format_exc())









# import tkinter as tk
# import MainFrame, ActionFrame

# def close_window():
#     ActionFrame.stop_camera()
#     root.destroy()

# def navigate_to_main_screen():
#     ActionFrame.stop_camera()
#     ActionFrame.hide() # Hide the action frame
#     MainFrame.pack()  # Show the main frame

# def open_action_screen():
#     # Check if the camera is successfully opened
#     if not ActionFrame.start_camera():
#         # Return to the main screen if camera opening failed
#         return
#     # Hide the main frame
#     MainFrame.hide()
#     # Show the action frame
#     ActionFrame.pack()

# root = tk.Tk()
# root.title("SIGNiT")
# # Create and show Main screen
# MainFrame.init(root, open_action_screen)
# ActionFrame.init(root, close_window, navigate_to_main_screen)
# root.mainloop()






