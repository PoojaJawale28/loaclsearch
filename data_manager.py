import csv
import os
from tkinter import messagebox

class DataManager:
    def __init__(self, filename='businesses.csv'):
        self.filename = filename
        # Define expected headers for robust loading and saving
        self.expected_headers = ['ID', 'Name', 'Category', 'Address', 'Phone', 'Website', 'Hours', 'Description', 'Latitude', 'Longitude']

    def load_business_data(self):
        """Loads business data from a CSV file.
        Returns a list of dictionaries, or None on critical error."""
        businesses = []
        if not os.path.exists(self.filename):
            # Create an empty CSV with headers if it doesn't exist
            try:
                with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.expected_headers)
                return []
            except Exception as e:
                messagebox.showerror("File Creation Error", f"Could not create '{self.filename}': {e}")
                return None # Indicate critical error

        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Check for essential columns, but proceed if they are missing (data will be N/A)
                if not all(col in reader.fieldnames for col in ['Name', 'Category', 'Address', 'Phone']):
                    messagebox.showwarning("Warning", f"CSV file '{self.filename}' might be missing essential columns (Name, Category, Address, Phone).")
                
                for row in reader:
                    # Fill missing expected headers with empty string to prevent KeyError later
                    processed_row = {header: row.get(header, '') for header in self.expected_headers}
                    businesses.append(processed_row)
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading business data from '{self.filename}': {e}")
            return None # Indicate critical error
        return businesses

    def save_business_data(self, businesses_list):
        """Saves current business data to the CSV file."""
        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.expected_headers)
                writer.writeheader()
                writer.writerows(businesses_list)
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving data to '{self.filename}': {e}")
            return False

