
```markdown
# Web Page Downloader and Link Extractor

Welcome to the Web Page Downloader and Link Extractor project! This project includes two Python scripts for extracting HTML links and downloading web pages along with their assets.

## Project Description

This project consists of two Python scripts:
1. **Extract Links**: Extracts all HTML links from a given base URL and saves them to a text file.
2. **Download Pages**: Downloads HTML pages and their associated assets (CSS, JS, images) from a list of URLs and compresses them into ZIP files.

## Technologies Used

- **Backend**: Python
- **Libraries**: `requests`, `beautifulsoup4`
- **Compression**: `zipfile`

## Project Setup Guide

Follow these simple steps to set up and run the project:

1. **Install Dependencies**: Install the required Python libraries using the following command:
   ```bash
   pip install requests beautifulsoup4
   ```

2. **Run Extract Links Script**:
   - Update the `base_url` variable in `extract_links.py` with the URL you want to extract links from.
   - Execute the script:
     ```bash
     python extract_links.py
     ```

3. **Run Download Pages Script**:
   - Update the `urls_to_download` list in `download_pages.py` with the URLs you want to download.
   - Execute the script:
     ```bash
     python download_pages.py
     ```

## Output

- **Extract Links**: Links will be saved in `list_of_domains.txt`, formatted with single quotes.
- **Download Pages**: Each URL will be downloaded and saved into its own folder, which will then be compressed into a ZIP file.

## Additional Information

- **Extract Links**: This script retrieves and saves all HTML links from a base URL. Useful for collecting URLs for further processing.
- **Download Pages**: This script downloads pages and their assets, organizing them into folders and compressing them into ZIP files. Ideal for archiving websites or offline viewing.

Enjoy using the project and feel free to contribute!
