import requests
from zipfile import ZipFile
import os


def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def extract_zip(zip_path, extract_to):
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def main():
    download_url = "https://github.com/atom0s/Steamless/releases/download/v3.1.0.3/Steamless.v3.1.0.3.-.by.atom0s.zip"
    zip_name = "Steamless.v3.1.0.3.-.by.atom0s.zip"

    # Determine the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path where the zip will be saved
    zip_path = os.path.join(script_dir, zip_name)

    # Download the zip file
    print(f"Downloading {zip_name}...")
    download_file(download_url, zip_path)
    print(f"Downloaded {zip_name} successfully.")

    # Define the directory to extract the contents
    extract_dir = os.path.join(script_dir, "Steamless.v3.1.0.3.-.by.atom0s")

    # Extract the zip file
    print(f"Extracting {zip_name}...")
    extract_zip(zip_path, extract_dir)
    print(f"Extracted {zip_name} successfully.")

    # Optionally, delete the zip file after extraction
    os.remove(zip_path)
    print(f"Deleted {zip_name}.")
    print("Finished installing Steamless.")


if __name__ == "__main__":
    main()
