# business_app.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
import uuid # For generating unique IDs

# Import external modules
from data_manager import DataManager
from map_utils import show_on_map
from dialog_utils import custom_confirm_dialog

class BusinessSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Local Business Search Engine")
        master.geometry("800x600") # Set a larger default window size
        master.resizable(True, True) # Allow window resizing

        self.data_manager = DataManager() # Instantiate the DataManager
        
        # --- Data Loading ---
        self.businesses = self.data_manager.load_business_data()
        if self.businesses is None: # None indicates a critical error during load
            master.destroy()
            return
        elif not self.businesses:
            messagebox.showwarning("Warning", "No business data found. 'businesses.csv' is empty or missing. You can add new businesses.")

        # --- UI Elements ---
        self.create_widgets()
        self.search_business() # Display all businesses initially

    def create_widgets(self):
        """Creates all UI elements for the main application window."""
        # --- Search Frame ---
        search_frame = tk.Frame(self.master, padx=10, pady=10)
        search_frame.pack(fill=tk.X)

        tk.Label(search_frame, text="Search for a business:").pack(side=tk.LEFT, padx=(0, 10))

        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.search_entry.bind("<Return>", self.search_business_event) # Allow Enter key to trigger search

        self.search_button = tk.Button(search_frame, text="Search", command=self.search_business)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))

        # --- Management and Sort Buttons Frame ---
        manage_sort_frame = tk.Frame(self.master, padx=10, pady=5)
        manage_sort_frame.pack(fill=tk.X)

        self.add_button = tk.Button(manage_sort_frame, text="Add New Business", command=self.open_add_edit_window)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = tk.Button(manage_sort_frame, text="Clear Search", command=self.clear_search)
        self.clear_button.pack(side=tk.LEFT, padx=(5, 15)) # Added Clear Search button

        # Sorting Options
        tk.Label(manage_sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=(0, 5))
        self.sort_option_var = tk.StringVar(self.master)
        self.sort_options = {
            "Name (A-Z)": ("Name", False),
            "Name (Z-A)": ("Name", True),
            "Category (A-Z)": ("Category", False),
            "Category (Z-A)": ("Category", True)
        }
        # Set default sort option
        self.sort_option_var.set(list(self.sort_options.keys())[0]) 

        self.sort_menu = tk.OptionMenu(manage_sort_frame, self.sort_option_var, *self.sort_options.keys(), command=self.search_business)
        self.sort_menu.pack(side=tk.LEFT, expand=False, fill=tk.X) # Removed expand=True

        # --- Results Area ---
        results_frame = tk.Frame(self.master, padx=10, pady=5)
        results_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(results_frame, text="Search Results:").pack(anchor=tk.NW, pady=(0,5))

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, font=("Arial", 10),
                                                    state=tk.DISABLED, # Start as read-only
                                                    height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # --- Status Bar ---
        self.status_bar = tk.Label(self.master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def search_business_event(self, event):
        """Event handler for Enter key press in search entry."""
        self.search_business()

    def _sort_results(self, results):
        """Helper method to sort the list of business results."""
        selected_option = self.sort_option_var.get()
        sort_key_name, reverse_sort = self.sort_options.get(selected_option, ("Name", False)) # Default to Name A-Z

        # Sort the results based on the chosen key
        # Using .get() with a default empty string to handle missing keys gracefully
        return sorted(results, key=lambda b: b.get(sort_key_name, '').lower(), reverse=reverse_sort)


    def search_business(self, *args): # *args to accept event from OptionMenu
        """Performs the business search and displays results."""
        query = self.search_entry.get().strip().lower()
        
        self.results_text.config(state=tk.NORMAL) # Enable text widget for editing
        self.results_text.delete(1.0, tk.END)  # Clear previous results

        found_results = []
        if not query:
            # If query is empty, show all businesses
            found_results = list(self.businesses)
            self.status_bar.config(text=f"Displaying all {len(found_results)} business(es).")
        else:
            for b in self.businesses:
                # More flexible searching: check if query is a substring of name, category, or description
                name_match = query in b.get('Name', '').lower()
                category_match = query in b.get('Category', '').lower()
                description_match = query in b.get('Description', '').lower()
                if name_match or category_match or description_match:
                    found_results.append(b)
            self.status_bar.config(text=f"Found {len(found_results)} result(s).")

        # Apply sorting to the found results
        found_results = self._sort_results(found_results)

        if found_results:
            for b in found_results:
                # Insert business details
                self.results_text.insert(tk.END, f"Name: {b.get('Name', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Category: {b.get('Category', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Address: {b.get('Address', 'N/A')}\n")
                self.results_text.insert(tk.END, f"Phone: {b.get('Phone', 'N/A')}\n")
                if b.get('Website'):
                    self.results_text.insert(tk.END, f"Website: {b['Website']}\n")
                if b.get('Hours'):
                    self.results_text.insert(tk.END, f"Hours: {b['Hours']}\n")
                if b.get('Description'):
                    self.results_text.insert(tk.END, f"Description: {b['Description']}\n")
                
                # Add action buttons for each business
                # Using a lambda to pass the specific business 'b' to the command
                self.results_text.insert(tk.END, "Actions: ")
                self.results_text.window_create(tk.END, window=tk.Button(self.results_text, text="Edit",
                                                    command=lambda data=b: self.open_add_edit_window(data),
                                                    font=("Arial", 8), padx=2, pady=0))
                self.results_text.insert(tk.END, " ")
                self.results_text.window_create(tk.END, window=tk.Button(self.results_text, text="Delete",
                                                    command=lambda data=b: self.delete_business(data),
                                                    font=("Arial", 8), padx=2, pady=0))
                self.results_text.insert(tk.END, " ")
                if b.get('Address') and b.get('Name'): # Only show map button if address and name exist
                     self.results_text.window_create(tk.END, window=tk.Button(self.results_text, text="Map",
                                                         command=lambda name=b.get('Name', ''), addr=b.get('Address', ''): show_on_map(name, addr, self.status_bar),
                                                         font=("Arial", 8), padx=2, pady=0))
                self.results_text.insert(tk.END, "\n\n") # Separator between businesses
        else:
            self.results_text.insert(tk.END, "No results found for your query. Try adding a new business!")
            self.status_bar.config(text="No results found.")

        self.results_text.config(state=tk.DISABLED) # Make text read-only again

    def clear_search(self):
        """Clears the search entry, results text, and displays all businesses."""
        self.search_entry.delete(0, tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_bar.config(text="Ready")
        self.search_business() # Re-display all businesses


    def open_add_edit_window(self, business_data=None):
        """Opens a Toplevel window for adding or editing business details."""
        add_edit_window = tk.Toplevel(self.master)
        add_edit_window.title("Edit Business" if business_data else "Add New Business")
        add_edit_window.geometry("500x450")
        add_edit_window.transient(self.master) # Make it appear on top of the main window
        add_edit_window.grab_set() # Make it modal

        frame = tk.Frame(add_edit_window, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Define entry fields
        fields = [
            ('Name', 'name_entry'),
            ('Category', 'category_entry'),
            ('Address', 'address_entry'),
            ('Phone', 'phone_entry'),
            ('Website', 'website_entry'),
            ('Hours', 'hours_entry'),
            ('Description', 'description_entry'),
            ('Latitude', 'latitude_entry'),
            ('Longitude', 'longitude_entry')
        ]
        
        # Store entry widgets in a dictionary for easy access
        self.add_edit_entries = {} 

        for i, (label_text, entry_key) in enumerate(fields):
            tk.Label(frame, text=f"{label_text}:").grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            
            if entry_key == 'description_entry':
                entry = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=4, width=40, font=("Arial", 10))
                entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
            else:
                entry = tk.Entry(frame, width=40)
                entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.EW)
            
            self.add_edit_entries[entry_key] = entry

            # Populate fields if editing an existing business
            if business_data:
                # Map CSV keys to entry widget keys
                csv_key_map = {
                    'name_entry': 'Name', 'category_entry': 'Category', 'address_entry': 'Address',
                    'phone_entry': 'Phone', 'website_entry': 'Website', 'hours_entry': 'Hours',
                    'description_entry': 'Description', 'latitude_entry': 'Latitude', 'longitude_entry': 'Longitude'
                }
                for entry_k, csv_k in csv_key_map.items():
                    if entry_k == entry_key and business_data.get(csv_k):
                        if entry_key == 'description_entry':
                            entry.insert(tk.END, business_data[csv_k])
                        else:
                            entry.insert(0, business_data[csv_k])

        # Save and Cancel buttons
        button_frame = tk.Frame(frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Save", command=lambda: self.save_add_edit_business(business_data, add_edit_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=add_edit_window.destroy).pack(side=tk.LEFT, padx=5)

        add_edit_window.columnconfigure(1, weight=1) # Allow the entry column to expand
        add_edit_window.protocol("WM_DELETE_WINDOW", add_edit_window.destroy) # Handle window close button
        self.master.wait_window(add_edit_window) # Wait for add/edit window to close

    def save_add_edit_business(self, original_business_data, window):
        """Saves or updates a business entry."""
        new_data = {}
        for key, entry_widget in self.add_edit_entries.items():
            if isinstance(entry_widget, scrolledtext.ScrolledText):
                new_data[key.replace('_entry', '').capitalize()] = entry_widget.get("1.0", tk.END).strip()
            else:
                new_data[key.replace('_entry', '').capitalize()] = entry_widget.get().strip()

        # Basic validation
        if not new_data.get('Name') or not new_data.get('Category') or not new_data.get('Address'):
            messagebox.showwarning("Input Error", "Name, Category, and Address are required fields.")
            return

        if original_business_data: # Editing existing business
            # Find the business by its ID (preferred) or name and update it
            found = False
            for i, b in enumerate(self.businesses):
                if b.get('ID') == original_business_data.get('ID'):
                    # Update all fields
                    for key_map, csv_key in {
                        'name_entry': 'Name', 'category_entry': 'Category', 'address_entry': 'Address',
                        'phone_entry': 'Phone', 'website_entry': 'Website', 'hours_entry': 'Hours',
                        'description_entry': 'Description', 'latitude_entry': 'Latitude', 'longitude_entry': 'Longitude'
                    }.items():
                        b[csv_key] = new_data.get(csv_key, '') # Use .get with empty string default
                    found = True
                    break
            if not found:
                messagebox.showerror("Error", "Could not find business to edit.")
                return
            messagebox.showinfo("Success", "Business updated successfully!")
        else: # Adding new business
            new_data['ID'] = str(uuid.uuid4()) # Generate a unique ID
            # Ensure all expected headers are present, even if empty
            for header in self.data_manager.expected_headers: # Use expected headers from DataManager
                if header not in new_data:
                    new_data[header] = ''
            self.businesses.append(new_data)
            messagebox.showinfo("Success", "New business added successfully!")

        if self.data_manager.save_business_data(self.businesses): # Call DataManager to save
            window.destroy()
            self.search_business() # Refresh results in main window
        else:
            # Error message already shown by DataManager
            pass

    def delete_business(self, business_data):
        """Deletes a business entry after confirmation."""
        # Use the custom confirmation dialog from dialog_utils
        if custom_confirm_dialog(self.master, "Confirm Delete", f"Are you sure you want to delete '{business_data.get('Name', 'N/A')}'?"):
            try:
                # Filter out the business to be deleted by its ID
                self.businesses = [b for b in self.businesses if b.get('ID') != business_data.get('ID')]
                if self.data_manager.save_business_data(self.businesses): # Call DataManager to save
                    messagebox.showinfo("Success", "Business deleted successfully!")
                    self.search_business() # Refresh results
                else:
                    # Error message already shown by DataManager
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete business: {e}")

