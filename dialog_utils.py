# dialog_utils.py
import tkinter as tk

def custom_confirm_dialog(master, title, message):
    """A simple custom confirmation dialog using Toplevel."""
    confirm_window = tk.Toplevel(master)
    confirm_window.title(title)
    confirm_window.geometry("300x120")
    confirm_window.transient(master)
    confirm_window.grab_set() # Make it modal

    result = False # Default to False (No)

    tk.Label(confirm_window, text=message, wraplength=280).pack(pady=10)

    button_frame = tk.Frame(confirm_window)
    button_frame.pack(pady=5)

    def set_result_and_destroy(value):
        nonlocal result
        result = value
        confirm_window.destroy()

    tk.Button(button_frame, text="Yes", command=lambda: set_result_and_destroy(True)).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="No", command=lambda: set_result_and_destroy(False)).pack(side=tk.LEFT, padx=10)

    # Wait for the confirmation window to close before returning a result
    master.wait_window(confirm_window)
    return result

