# Spotify Play Count Scraper

This program scrapes the play counts of Spotify tracks using the Selenium WebDriver. It retrieves the play counts for a list of track IDs and stores the results in a Pandas DataFrame.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)


## Features

- Scrapes play counts from Spotify tracks.
- Uses Selenium for web scraping with headless Chrome.
- Supports scraping multiple tracks in a loop.
- Outputs results in a Pandas DataFrame.

## Requirements

- Python 3.x
- Selenium
- Pandas
- ChromeDriver (automatically installed with the script)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/spotify-play-count-scraper.git
   cd spotify-play-count-scraper

2. Install the required Python packages:

   ```bash
   
    pip install selenium pandas

4. If you are running this in a Colab environment, uncomment the following lines to install Chromium and ChromeDriver:

    ```bash
 
    !apt-get update
    !apt install -y chromium-chromedriver


## Usage


1. Prepare a Pandas DataFrame containing track IDs that you want to scrape. The DataFrame should have a column named Track ID.

2. The script constructs track URLs using the Track ID and initializes new columns for URLs and play counts.

3. Run the scraping function, which will populate the Play Count column with the corresponding play counts for each track.

4. Finally, the updated DataFrame with play counts can be displayed.


