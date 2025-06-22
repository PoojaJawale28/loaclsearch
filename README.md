# Local Business Search Engine 
This project is a desktop application built with Python's Tkinter library, designed to efficiently manage and search a local business directory. It demonstrates capabilities in desktop application development, data management, and user interface design.

### Features
Comprehensive Business Management:

* Add New Businesses: Easily input and save details for new local businesses.
* Edit Existing Businesses: Modify any aspect of a business's information.
* Delete Businesses: Securely remove entries from the directory with confirmation.

Flexible Search Functionality:

* Search businesses by Name, Category, or Description.
* "Clear Search" button to quickly reset the search and view all entries.

Dynamic Sorting:

* Sort search results by Name (A-Z, Z-A) and Category (A-Z, Z-A) for better organization.

Enhanced Business Details:

* Stores and displays extended information including Website, Hours of Operation, and a detailed Description.

Integrated Map View:

* Directly opens a business's location in Google Maps via your default web browser, leveraging Name and Address for precise mapping.

Modular Code Structure:

* The application's logic is cleanly separated into multiple Python files (main.py, business_app.py, data_manager.py, map_utils.py, dialog_utils.py) for improved maintainability and scalability.

CSV Data Persistence:

* All business data is stored and retrieved from a businesses.csv file, ensuring data persists across application sessions.

Technologies Used
* Python 3.x: The core programming language.
* Tkinter: Python's standard GUI toolkit for building the desktop interface.
* CSV Module: For handling data storage and retrieval in CSV format.
* webbrowser Module: For integrating external web services like Google Maps.
* uuid Module: For generating unique identifiers for business entries.
