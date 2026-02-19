import time
import random
import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import sys

# Init path to access shared utils
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from src.utils.config_loader import ConfigLoader

# --- CONSTANTS ---
STATE_FILE = "scraper_state_apartments.json"

def get_project_root():
    """Return absolute path to project root."""
    return project_root

def load_state():
    """Load scraping state (last visited page) from JSON."""
    state_path = os.path.join(get_project_root(), STATE_FILE)
    if os.path.exists(state_path):
        with open(state_path, 'r') as f:
            return json.load(f)
    return {"last_page": 0}

def save_state(page_number):
    """Save current scraping progress."""
    state_path = os.path.join(get_project_root(), STATE_FILE)
    with open(state_path, 'w') as f:
        json.dump({"last_page": page_number}, f)

def get_existing_urls(csv_path):
    """
    Load set of already scraped URLs to avoid duplicates.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        set: A set of URL strings.
    """
    if not os.path.exists(csv_path):
        return set()
    try:
        df = pd.read_csv(csv_path)
        if 'url' in df.columns:
            return set(df['url'].unique())
    except Exception:
        return set()
    return set()

def setup_driver(config):
    """
    Initialize Selenium WebDriver with configuration options.

    Args:
        config (dict): Global configuration dictionary.

    Returns:
        webdriver.Chrome: Initialized driver instance.
    """
    options = webdriver.ChromeOptions()
    if config['driver']['headless']:
        options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f"user-agent={config['driver']['user_agent']}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_apartment_data(element):
    """
    Parse a single apartment HTML element and extract details.

    Args:
        element (WebElement): The HTML element representing one ad card.

    Returns:
        dict: Extracted data (title, url, price, location) or None if failed.
    """
    data = {}
    try:
        # Title & Link (Updated selector)
        # Title is often in h2.c-products__title within the item
        try:
            title_el = element.find_element(By.CLASS_NAME, "c-products__title")
            data['title'] = title_el.text.strip()
            
            # Link is often on the main anchor wrapper .c-products__link
            # But we are inside .c-products__item which usually contains the link
            link_el = element.find_element(By.CLASS_NAME, "c-products__link")
            data['url'] = link_el.get_attribute("href")
        except:
             return None

        # Price (Updated selector)
        try:
            price_el = element.find_element(By.CLASS_NAME, "c-products__price")
            data['raw_price'] = price_el.text.strip()
        except:
            data['raw_price'] = "0"

        # Location (Updated selector)
        try:
            loc_el = element.find_element(By.CLASS_NAME, "c-products__info")
            data['location'] = loc_el.text.strip()
        except:
            data['location'] = ""

        return data
    except Exception:
        return None

def main():
    """
    Main execution loop for the scraper.
    """
    try:
        config = ConfigLoader.get_config()
    except Exception as e:
        print(f"Error: {e}")
        return

    scraper_cfg = config['scraper']
    paths_cfg = config['paths']
    
    output_dir = os.path.join(get_project_root(), paths_cfg['output_folder'])
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, paths_cfg['output_filename'])

    state = load_state()
    start_page = state['last_page'] + 1
    seen_urls = get_existing_urls(output_path)

    print(f"--- INFO: Loaded {len(seen_urls)} apartments. Resuming from page {start_page}. ---")
    
    if start_page > scraper_cfg['num_pages']:
        print(f"\n⚠️  WARNING: Start page ({start_page}) is greater than configured 'num_pages' ({scraper_cfg['num_pages']}).")
        print("   The scraper has nothing to do. Increase 'num_pages' in config.json or delete 'scraper_state_apartments.json' to restart.")
        return

    driver = setup_driver(config)
    try:
        print("\n" + "=" * 50)
        print("⚠️  MANUAL INTERVENTION REQUIRED")
        print("1. Browser opens. Click 'Souhlasím' (Agree) on cookies.")
        print("2. Press ENTER here in terminal to continue.")
        print("=" * 50 + "\n")

        # Initial load to handle cookies
        driver.get(scraper_cfg['base_url'])
        input(">>> Press ENTER here after cookies are handled... <<<")

        for page_num in range(start_page, scraper_cfg['num_pages'] + 1):
            # Using 'page' parameter as seen in browser, though 'strana' might work too
            url = f"{scraper_cfg['base_url']}?page={page_num}"
            print(f"Loading Page {page_num}: {url}")
            driver.get(url)
            
            # Random delay
            time.sleep(random.uniform(2, 4))
            
            # Scroll down to ensure images/items load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Find items (Updated Selector)
            items = driver.find_elements(By.CLASS_NAME, "c-products__item")
            
            page_data = []
            for item in items:
                data = extract_apartment_data(item)
                if data and data.get('url') and data['url'] not in seen_urls:
                    seen_urls.add(data['url'])
                    page_data.append(data)

            if page_data:
                df = pd.DataFrame(page_data)
                header = not os.path.exists(output_path)
                df.to_csv(output_path, mode='a', header=header, index=False, encoding='utf-8')
                print(f"   -> Saved {len(page_data)} new apartments.")
            else:
                 print("   -> No new unique apartments found on this page.")

            save_state(page_num)

    except KeyboardInterrupt:
        print("\n--- SCRAPING PAUSED BY USER ---")

    except Exception as e:
         print(f"Critical Error: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
