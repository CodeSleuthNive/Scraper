#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# # Install necessary dependencies (if running in Colab)
# !apt-get update
# !apt install -y chromium-chromedriver
# !pip install selenium pandas

# Import required libraries
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Selenium with headless Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Function to scrape play count for a given track URL
def scrape_play_count(track_url):
    try:
        # Load the track URL
        driver.get(track_url)
        
        # Wait for the play count element to load
        play_count_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-testid='playcount']"))
        )
        
        # Extract and return the play count text
        play_count = play_count_element.text.strip()
        return play_count
    except Exception as e:
        print(f"Error scraping {track_url}: {e}")
        return None



# Initialize new columns for URLs and play counts
df['Track URL'] = 'https://open.spotify.com/track/' + df['Track ID']
df['Play Count'] = None  # Initialize with None

# Scrape play counts for each track URL with waiting time
for index, row in df.iterrows():
    track_url = row['Track URL']
    print(f"Scraping play count for: {track_url}")
    play_count = scrape_play_count(track_url)
    df.at[index, 'Play Count'] = play_count  # Update the DataFrame
    
    # Wait for 3 seconds between requests to avoid being blocked
    time.sleep(3)

# Close the WebDriver
driver.quit()

# Display the updated DataFrame
display(df)

