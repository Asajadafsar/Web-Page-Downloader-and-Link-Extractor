import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_html_links(base_url, max_pages=100):
    """
    Fetch HTML links from a base URL and return a set of unique HTML links.
    """
    visited = set()  # Keep track of visited URLs
    to_visit = [base_url]  # Start with the base URL
    html_links = set()  # Set to store unique HTML links
    
    while to_visit and len(html_links) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find and process all links on the page
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                full_url = urljoin(base_url, href)
                
                if full_url.endswith('.html'):
                    # Ensure the URL belongs to the same domain
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        if full_url not in html_links:
                            html_links.add(full_url)
                            to_visit.append(full_url)

        except requests.RequestException as e:
            print(f"Error fetching {current_url}: {e}")
    
    return html_links

def save_links_to_file(links, file_path):
    """
    Save the set of links to a text file, formatted with single quotes and trailing commas.
    """
    with open(file_path, 'w') as file:
        for link in links:
            file.write(f"'{link}',\n")
    print(f"Links saved to {file_path}")

if __name__ == "__main__":
    base_url = "test.ir/index.html"  # Replace with your URL
    output_file = "list_of_domains.txt"
    html_links = fetch_html_links(base_url)
    save_links_to_file(html_links, output_file)
