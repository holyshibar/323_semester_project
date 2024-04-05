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


def download_steamless():
    download_url = "https://github.com/atom0s/Steamless/releases/download/v3.1.0.3/Steamless.v3.1.0.3.-.by.atom0s.zip"
    # Define the directory to extract the contents
    extract_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Steamless.v3.1.0.3.-.by.atom0s")
    download_and_extract(download_url, extract_dir)


def download_goldberg():
    download_url = "https://gitlab.com/Mr_Goldberg/goldberg_emulator/uploads/2524331e488ec6399c396cf48bbe9903/Goldberg_Lan_Steam_Emu_v0.2.5.zip"
    extract_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Goldberg_Lan_Steam_Emu_v0.2.5")
    download_and_extract(download_url, extract_dir)


def download_and_extract(url, extract_dir):
    zip_name = os.path.basename(url)
    # Determine the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path where the zip will be saved
    zip_path = os.path.join(script_dir, zip_name)
    # Download the zip file
    print(f"Downloading {zip_name}...")
    download_file(url, zip_path)
    print(f"Downloaded {zip_name} successfully.")
    # Extract the zip file
    print(f"Extracting {zip_name}...")
    extract_zip(zip_path, extract_dir)
    print(f"Extracted {zip_name} successfully.")
    # Optionally, delete the zip file after extraction
    os.remove(zip_path)
    print(f"Deleted {zip_name}.")

