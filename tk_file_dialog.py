import tkinter as tk
from tkinter import filedialog

def CreateFileDialog_Open():
    global f_path
    f_path = filedialog.askopenfilename(
        title="Choose image cover...",
        filetypes=[("Images", "*.png *.jpg" "*.jpeg *.bmp" "*.webp" "*.tiff"), ("All files", "*.*")]
    )
    if f_path:

        print("File opened: ", f_path)
    else:
        pass
    return f_path

def CreateFileDialog_OpenFolder():
    global directory_folder_path
    directory_folder_path = filedialog.askdirectory(
        title="Choose folder...",
    )
    if directory_folder_path:
        print("Directory opened: ", directory_folder_path)
    else:
        pass
    return directory_folder_path

def CreateFileDialog_SaveToFolder():
    global folder_path
    folder_path = filedialog.asksaveasfilename(
        title="Choose folder...",
        defaultextension=".txt",
        initialfile="1.png",
        filetypes=[("Images", "*.png *.jpg"), ("All files", "*.*")]
    )
    if folder_path:
        print("Saved into: ", folder_path)
    else:
        pass
    return folder_path
