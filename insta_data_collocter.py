
import random
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Mobile Safari/537.36"
]

username = os.getenv("INSTAGRAM_USERNAME", "your username")  
password = os.getenv("INSTAGRAM_PASSWORD", "password")

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent={random.choice(user_agents)}")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)  
username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
username_input.send_keys(username)

password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
password_input.send_keys(password)

login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
login_button.click()

time.sleep(10)

def scrape_instagram_data(url):
    retries = 3  # Number of retries
    for attempt in range(retries):
        try:
            

            # Open Instagram Profile
            driver.get(url)
            time.sleep(5)  # Wait for page to load

            # Extract HTML and close the driver
            page_source = driver.page_source

            # Parse with BeautifulSoup
            soup = BeautifulSoup(page_source, "html.parser")

            # Extract name, bio, posts
            name = soup.find("h2").text if soup.find("h2") else "Not found"
            bio_meta = soup.find("meta", {"name": "description"})
            bio = bio_meta["content"] if bio_meta else "Not found"

            post_meta = soup.find("meta", property="og:description")
            post_count = post_meta["content"].split(",")[0] if post_meta else "Not found"

            story_section = soup.find("div", {"role": "presentation"})
            story_text = story_section.text.strip() if story_section else "No story text found"

            if "Not found" not in [name, bio, post_count]:
                return (url, name, bio, post_count, story_text)

            print(f"Attempt {attempt + 1} failed for {url}. Retrying...")
            time.sleep(3)

        except Exception as e:
            print(f"Error on attempt {attempt + 1} for {url}: {e}")
            time.sleep(5)

    return (url, "Not found", "Not found", "Not found", "No story text found")

def process_csv(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader, None)  
        
        with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['URL', 'Name', 'Bio', 'Posts', 'Story Text'])
            
            for row in reader:
                url = row[0]
                print(f"Scraping data for: {url}")
                data = scrape_instagram_data(url)
                writer.writerow(data)
                print(f"Data for {url} written to CSV.")

input_csv = "C:/Users/Al Rehman Computers/Desktop/db/insta.csv"
output_csv = "C:/Users/Al Rehman Computers/Desktop/db/output.csv"

process_csv(input_csv, output_csv)
driver.quit()
