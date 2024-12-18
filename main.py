import pandas as pd
import time
import json
import random
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

def get_random_delay():
    base_delay = random.uniform(2, 5)
    if random.random() < 0.1:
        base_delay += random.uniform(3, 7)
    return base_delay

def setup_driver(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    ua = UserAgent()
    chrome_options.add_argument(f'user-agent={ua.random}')
    
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def check_wallet_eligibility(driver, wallet_address, max_retries=3):
    url = f"https://api.clusters.xyz/v0.1/airdrops/pengu/eligibility/{wallet_address}"
    
    retries = 0
    while retries < max_retries:
        try:
            driver.set_script_timeout(random.uniform(10, 15))
            driver.get(url)
            time.sleep(random.uniform(1, 2))
            
            pre_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(('tag name', 'pre'))
            )
            
            time.sleep(random.uniform(0.5, 1))
            response_text = pre_element.text
            data = json.loads(response_text)
            
            return {
                'wallet_address': wallet_address,
                'total': int(data.get('total', 0)),
                'total_unclaimed': int(data.get('totalUnclaimed', 0))
            }
            
        except Exception as e:
            print(f"Attempt {retries + 1} failed for wallet {wallet_address}: {str(e)}")
            retries += 1
            if retries < max_retries:
                delay = (2 ** retries) + random.uniform(1, 3)
                time.sleep(delay)
    
    return {
        'wallet_address': wallet_address,
        'total': 0,
        'total_unclaimed': 0
    }

def save_result(result, output_file):
    """Save single result to CSV file"""
    df = pd.DataFrame([result])
    
    if Path(output_file).exists():
        df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        df.to_csv(output_file, index=False)

def get_processed_wallets(output_file):
    """Get list of already processed wallets"""
    if Path(output_file).exists():
        try:
            df = pd.read_csv(output_file)
            return set(df['wallet_address'].values)
        except Exception as e:
            print(f"Error reading existing results file: {e}")
    return set()

def process_wallets(input_file, output_file, proxies=None, batch_size=50):
    # Read input wallets
    wallets_df = pd.read_csv(input_file, header=None, names=['wallet_address'])
    all_wallets = set(wallets_df['wallet_address'].values)
    
    # Get already processed wallets
    processed_wallets = get_processed_wallets(output_file)
    wallets_to_process = list(all_wallets - processed_wallets)
    
    if not wallets_to_process:
        print("All wallets have been already processed!")
        return
    
    print(f"Found {len(processed_wallets)} already processed wallets")
    print(f"Remaining wallets to process: {len(wallets_to_process)}")
    
    total_wallets = len(wallets_to_process)
    total_airdrop = 0
    
    # Process in batches
    for batch_start in range(0, total_wallets, batch_size):
        batch_end = min(batch_start + batch_size, total_wallets)
        batch_wallets = wallets_to_process[batch_start:batch_end]
        
        print(f"\nProcessing batch {batch_start//batch_size + 1}")
        
        driver = setup_driver()
        
        try:
            for index, wallet in enumerate(batch_wallets, 1):
                print(f"Processing wallet {batch_start + index}/{total_wallets}: {wallet}")
                
                result = check_wallet_eligibility(driver, wallet)
                total_airdrop += result['total']
                
                # Save result immediately after processing each wallet
                save_result(result, output_file)
                print(f"Saved result for wallet: {wallet}")
                
                time.sleep(get_random_delay())
                
        finally:
            driver.quit()
        
        # Delay between batches
        batch_delay = random.uniform(10, 20)
        print(f"Batch completed. Waiting {batch_delay:.1f} seconds before next batch...")
        time.sleep(batch_delay)
    
    print(f"\nAll results saved to {output_file}")
    print(f"Total airdrop amount for this session: {total_airdrop}")

if __name__ == "__main__":
    input_file = "wallets.csv"
    output_file = "results.csv"
    
    if not Path(input_file).exists():
        print(f"Error: Input file {input_file} not found")
        exit(1)
    
    process_wallets(input_file, output_file)