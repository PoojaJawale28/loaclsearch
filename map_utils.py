import webbrowser
from tkinter import messagebox

def show_on_map(name, address, status_bar=None):
    """Opens the business address and name in Google Maps in the default web browser."""
    if not address and not name:
        messagebox.showwarning("Map Error", "No name or address available for this business.")
        if status_bar:
            status_bar.config(text="Map error: No data available.")
        return

    # Concatenate name and address for the query
    query_string = f"{name} {address}".strip()
    map_url = f"https://www.google.com/maps/search/?api=1&query={query_string.replace(' ', '+')}"
    try:
        webbrowser.open_new_tab(map_url)
        if status_bar:
            status_bar.config(text=f"Opening map for {name} at {address}...")
    except Exception as e:
        messagebox.showerror("Map Error", f"Could not open map: {e}")
        if status_bar:
            status_bar.config(text="Failed to open map.")

