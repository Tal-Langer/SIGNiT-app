from cx_Freeze import setup, Executable
import os

os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python38\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python38\tcl\tcl8.6'

# Define files/directories that should be included as is
# include_files = ['GUI/', 'Model/']
include_files = ['GUI/Images/', 'Model/']


# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"packages": ["tkinter", "os", "GUI"], "include_files": include_files, "includes": ["Controllers"]}
# build_exe_options = {
#     "packages": ["tkinter", "os", "GUI"],
#     "include_files": include_files,
#     "includes": ["GUI/Controllers"]
# }
build_exe_options = {
    "packages": ["tkinter", "os", "GUI", "GUI.Controllers"],
    "include_files": include_files
}



setup(
    name = "SIGNiT",
    version = "0.1",
    description = "Your description",
    options = {"build_exe": build_exe_options},
    executables = [Executable("GUI/UI.py")]
)
