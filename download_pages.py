#library python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import zipfile
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading



#Get urls
#check Urls Not agin
#Get and save Urls
#processing and save css/js/images and....
def fetch_and_save_html_resources(base_url, urls, output_dir):
    """
    Fetch and save specified HTML pages and their resources (CSS, JS, images) from the base URL to the specified directory.
    """
    visited = set()

    for url in urls:
        current_url = url.strip()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save HTML content
            path = urlparse(current_url).path
            if path == '':
                path = '/index.html'
            file_path = os.path.join(output_dir, path.lstrip('/'))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)

            # Process and save CSS, JS, and images
            for resource_type, attr in [('link', 'href'), ('script', 'src'), ('img', 'src')]:
                for resource in soup.find_all(resource_type, **{attr: True}):
                    src = resource.get(attr)
                    full_url = urljoin(current_url, src)
                    resource_path = urlparse(full_url).path
                    if resource_path:
                        resource_file_path = os.path.join(output_dir, resource_path.lstrip('/'))
                        if not os.path.exists(resource_file_path):
                            try:
                                res = requests.get(full_url)
                                res.raise_for_status()
                                os.makedirs(os.path.dirname(resource_file_path), exist_ok=True)
                                with open(resource_file_path, 'wb') as file:
                                    file.write(res.content)
                            except requests.RequestException as e:
                                print(f"Error fetching resource {full_url}: {e}")

        except requests.RequestException as e:
            print(f"Error fetching {current_url}: {e}")



#convert zip
def save_to_zip(output_dir, zip_path):
    """
    Compress the output directory into a ZIP file.
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_dir))
    print(f"Files saved to {zip_path}")



#get urls
#processing in background system
#save zip
def start_scraping():
    """
    Extract and save the specified HTML pages and their resources.
    """
    urls = url_entry.get("1.0", ctk.END).strip().split("\n")
    if not urls:
        messagebox.showerror("Input Error", "Please enter URLs")
        return

    output_dir = 'website_resources'

    def worker():
        status_label.configure(text="Scraping in progress...")
        fetch_and_save_html_resources("", urls, output_dir)

        # Ask user where to save the ZIP file
        zip_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])
        if zip_path:
            try:
                save_to_zip(output_dir, zip_path)
                messagebox.showinfo("Saved", f"Files saved to {zip_path}")
            except IOError as e:
                messagebox.showerror("Save Error", f"Error saving file: {e}")

        status_label.configure(text="Scraping completed")

    # Run the worker function in a new thread
    threading.Thread(target=worker, daemon=True).start()




#User interface settings
app = ctk.CTk()
app.title("Website HTML Extractor")
app.geometry("600x400")

# Input Section
url_label = ctk.CTkLabel(app, text="Enter URLs (one per line):")
url_label.pack(pady=10)
url_entry = ctk.CTkTextbox(app, width=500, height=150)
url_entry.pack(pady=10)

# Buttons
start_button = ctk.CTkButton(app, text="Go to the site's address to get the source code output", command=start_scraping)
start_button.pack(pady=10)

# Output Section
status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

# Run the application
app.mainloop()
