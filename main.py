import logging
import os
import re

import requests
from concurrent.futures import ThreadPoolExecutor

from release.scraper.scraper import Scraper
from release.scraper.database import Database
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='scraping.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    scraper = Scraper()
    database = Database()

    num = get_valid_num()
    download_dir = None if num == 0 else get_valid_dir()

    all_volumes = scraper.get_all_volumes()

    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust max_workers as needed
        futures = []
        for volume_id in all_volumes:
            futures.append(executor.submit(scrape_volume, volume_id, scraper, database))
        for future in futures:
            future.result()

    for volume_id in all_volumes:
        if num is None or num > 0:
            download_paper(volume_id, database, download_dir)
            logging.info(f"Volume {volume_id} downloaded")
            if num is not None: num -= 1
        else: break

def scrape_volume(volume_id, scraper, database,):
    if database.volume_exists(volume_id):
        logging.info(f"Volume {volume_id} already in database")
    else:
        # Get and save volume to database
        volume_metadata = scraper.get_volume_metadata(volume_id)
        if volume_metadata is not None:
            volume_object_id = database.save_volume(volume_metadata.__dict__)

            # Get and save papers to database
            volume_papers = scraper.get_volume_papers(volume_id)
            for paper in volume_papers:
                paper.volume_id = volume_object_id
                database.save_paper(paper.__dict__)

def download_paper(volume_id, database, download_dir):
    volume_papers = database.get_papers(database.get_volume_id(volume_id))
    for paper in volume_papers:
        response = requests.get(paper['url'])
        os.makedirs(f"{download_dir}\\{volume_id}", exist_ok=True)
        match = re.search(r'/([^/]+)\.[^.]+$', paper['url']).group(1)
        file_name = f"{match}_{re.sub(r'[<>:"/\\|?*\n\r]+', "", paper['title'])}".strip()
        try:
            with open(f"{download_dir}\\{volume_id}\\{file_name}", "wb") as file:
                file.write(response.content)
        except (ValueError, OSError) as e:
            logging.error(f"Error downloading {paper['url']}: {e}")


def get_valid_num():
    while True:
        user_input = input("Enter the number of volumes to download (or leave blank to get all of them): ").strip()
        try:
            if user_input != "":
                return int(user_input)
            else:
                return None
        except ValueError:
            print("Invalid input! Please enter a valid number or a blank.")

def get_valid_dir():
    while True:
        folder_path = input("Enter a directory to save files (or press Enter for default): ").strip()

        if not folder_path:
            folder_path = os.path.join(os.getcwd(), "Downloads")  # Default to "Downloads" in current dir

        folder_path = os.path.expanduser(folder_path)

        try:
            os.makedirs(folder_path, exist_ok=True)
            return folder_path
        except OSError as e:
            print(f"Invalid directory: {e}. Please try again.")

if __name__ == "__main__":
    main()