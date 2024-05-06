import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to read JSON data
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to set up Chrome WebDriver
def setup_driver(driver_path):
    service = Service(driver_path)
    chrome_options = Options()
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape data for a single ID
def scrape_data(driver, txid):
    attempts = 0
    while attempts < 5:
        url = f"https://doge.ordinalswallet.com/inscription/{txid}"
        driver.get(url)
        time.sleep(.5)  # Wait before retrying
        try:
            title = driver.title
            seller_address_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "Details_linkValue___pLFY")]'))
            )
            seller_address = seller_address_element.text
            if seller_address != "link":
                return {'id': txid, 'title': title, 'seller_address': seller_address}
        except Exception as e:
            print(f"Error occurred for ID {txid}: {e}")
        attempts += 1
        
    return None

# Function to write data to JSON file
def write_to_json(file_path, data):
    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Main function
def main():
    json_data_path = 'C:/doginals-main/web_scraper/OW.json'
    output_json_path = 'C:/doginals-main/web_scraper/NerdStonsHolders.json'
    driver_path = 'C:/doginals-main/web_scraper/chromedriver.exe'

    data = read_json_file(json_data_path)
    driver = setup_driver(driver_path)

    with open(output_json_path, 'w', encoding='utf-8') as file:  # Create or clear the output file
        file.write("[")

    first_entry = True
    for item in data:
        result = scrape_data(driver, item['id'])
        if result:
            if not first_entry:
                with open(output_json_path, 'a', encoding='utf-8') as file:
                    file.write(", ")
            with open(output_json_path, 'a', encoding='utf-8') as file:
                json.dump(result, file, indent=4)
            first_entry = False

    with open(output_json_path, 'a', encoding='utf-8') as file:
        file.write("]")

    driver.quit()
    print("Scraping complete, data saved to OWjsonWepOut.json")

if __name__ == '__main__':
    main()
