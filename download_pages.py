import os
import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urljoin, urlparse
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def download_file(url, base_folder, session):
    """
    Download a file from a URL and save it to a folder, maintaining directory structure.
    """
    try:
        response = session.get(url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
        parsed_url = urlparse(url)
        path = parsed_url.path
        file_name = os.path.basename(path)
        
        # Handle empty file name (e.g., trailing slashes)
        if not file_name:
            file_name = 'index.html'
        
        # Create the folder structure
        folder_path = os.path.join(base_folder, os.path.dirname(path.lstrip('/')))
        os.makedirs(folder_path, exist_ok=True)
        
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def download_page(url, base_folder, session):
    """
    Download a page and its associated assets (CSS, JS, images) into the appropriate directories.
    """
    try:
        response = session.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Save the HTML page
        parsed_url = urlparse(url)
        path = parsed_url.path
        file_name = os.path.basename(path) or 'index.html'
        folder_path = os.path.join(base_folder, os.path.dirname(path.lstrip('/')))
        os.makedirs(folder_path, exist_ok=True)
        html_filename = os.path.join(folder_path, file_name)
        
        with open(html_filename, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        
        print(f"Downloaded {html_filename}")
        
        # Download linked CSS, JS, and images
        for tag in soup.find_all(['link', 'script', 'img']):
            src = tag.get('href') or tag.get('src')
            if src:
                asset_url = urljoin(url, src)
                asset_path = download_file(asset_url, base_folder, session)
                if asset_path:
                    # Update HTML references to local files
                    if tag.name == 'link':
                        tag['href'] = os.path.relpath(asset_path, base_folder)
                    elif tag.name == 'script':
                        tag['src'] = os.path.relpath(asset_path, base_folder)
                    elif tag.name == 'img':
                        tag['src'] = os.path.relpath(asset_path, base_folder)
        
        # Save updated HTML with local asset references
        with open(html_filename, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
    except requests.RequestException as e:
        print(f"Error downloading page {url}: {e}")

def download_website(url, output_folder):
    """
    Download the website and save it to a specified folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Create a session with retry mechanism
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))

    # Download the main page and assets
    download_page(url, output_folder, session)

def compress_folder(folder, output_zip):
    """
    Compress a folder into a ZIP file.
    """
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder))
    
    print(f"Compressed {folder} into {output_zip}")

def download_websites(urls):
    """
    Download multiple websites, each into its own folder and ZIP file.
    """
    for url in urls:
        domain = urlparse(url).netloc.replace('.', '_')
        output_folder = os.path.join('websites', domain)
        output_zip = f'{output_folder}.zip'
        
        print(f"Starting download for {url}")
        download_website(url, output_folder)
        compress_folder(output_folder, output_zip)
        print(f"Completed download for {url}")

# List of URLs to download
urls_to_download = [
    'https://themesflat.co/html/cointexcrypto/cointex/log-in.html',
    'https://themesflat.co/html/cointexcrypto/cointex/home.html',
    'https://themesflat.co/html/cointexcrypto/cointex/home-search.html',
    'https://themesflat.co/html/cointexcrypto/cointex/reset-pass.html',
    'https://themesflat.co/html/cointexcrypto/cointex/choose-bank.html',
    'https://themesflat.co/html/cointexcrypto/cointex/change-name.html',
    'https://themesflat.co/html/cointexcrypto/cointex/payment-confirm.html',
    'https://themesflat.co/html/cointexcrypto/cointex/wallet.html',
    'https://themesflat.co/html/cointexcrypto/cointex/list-blog.html',
    'https://themesflat.co/html/cointexcrypto/cointex/exchange-trade.html',
    'https://themesflat.co/html/cointexcrypto/cointex/choose-cryptocurrency.html',
    'https://themesflat.co/html/cointexcrypto/cointex/exchange.html',
    'https://themesflat.co/html/cointexcrypto/cointex/tell-us-more.html',
    'https://themesflat.co/html/cointexcrypto/cointex/register.html',
    'https://themesflat.co/html/cointexcrypto/cointex/exchange-trade-approve.html',
    'https://themesflat.co/html/cointexcrypto/cointex/cryptex-rating.html',
    'https://themesflat.co/html/cointexcrypto/cointex/verification.html',
    'https://themesflat.co/html/cointexcrypto/cointex/sell-quantity.html',
    'https://themesflat.co/html/cointexcrypto/cointex/security-center.html',
    'https://themesflat.co/html/cointexcrypto/cointex/user-info.html',
    'https://themesflat.co/html/cointexcrypto/cointex/qr-code.html',
    'https://themesflat.co/html/cointexcrypto/cointex/qr-code2.html',
    'https://themesflat.co/html/cointexcrypto/cointex/profile.html',
    'https://themesflat.co/html/cointexcrypto/cointex/recharge.html',
    'https://themesflat.co/html/cointexcrypto/cointex/exchange-market.html',
    'https://themesflat.co/html/cointexcrypto/cointex/change-password.html',
    'https://themesflat.co/html/cointexcrypto/cointex/buy-quantity.html',
    'https://themesflat.co/html/cointexcrypto/cointex/blog-detail.html',
    'https://themesflat.co/html/cointexcrypto/cointex/account-freeze.html',
    'https://themesflat.co/html/cointexcrypto/cointex/option.html',
    'https://themesflat.co/html/cointexcrypto/cointex/earn.html',
    'https://themesflat.co/html/cointexcrypto/cointex/verification-choose-type.html',
    'https://themesflat.co/html/cointexcrypto/cointex/choose-payment.html',

    # Add more URLs here
]

# Download all websites
download_websites(urls_to_download)
