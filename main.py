import tkinter as tk
from business_app import BusinessSearchApp # Import the main application class

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Instantiate and run the BusinessSearchApp
    # The BusinessSearchApp class handles all UI and logic orchestration
    app = BusinessSearchApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()
