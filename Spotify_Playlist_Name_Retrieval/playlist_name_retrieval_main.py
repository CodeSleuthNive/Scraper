#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
import time
import spotipy
import numpy as np
import pandas as pd
import re
from spotipy.oauth2 import SpotifyClientCredentials
import warnings
warnings.filterwarnings("ignore")
import datetime
from datetime import date
from datetime import timedelta
import sys
import traceback
from datetime import datetime




def get_playlist_id(queries, language):

    if not isinstance(queries, list):
        raise ValueError("Queries must be a list.")

    odia_terms = ['odia', 'oriya', 'ollywood', 'odisha']
    gujarati_terms = ['gujarat', 'gujarati', 'dhollywood', 'gujju']
    malayalam_terms = ['kerala', 'mollywood', ' malayalam', 'mallu']  # corrected spelling of 'ollywood'
    playlist_info = []

    try:
        Todays_TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Specify the directory path
        directory_path = r'/home/Nivetha/mnt/BACKUP_RUN_BY_MANUAL/Spotify_Playlist_Name_Retrieval'

        # Check if the directory exists, create it if not
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # Specify the file path
        xlsx_filename = os.path.join(directory_path, 'playlist_name_scrapping.xlsx')

        # Check if the xlsx file already exists, create it if not
        if not os.path.exists(xlsx_filename):
            pd.DataFrame().to_excel(xlsx_filename, index=False)

        # Read the existing DataFrame
        existing_df = pd.read_excel(xlsx_filename)

        for index, (search_query, language_1) in enumerate(zip(queries, language)):
            search_query_append = search_query  # corrected variable name
            search_results = sp.search(q=search_query, type='playlist', market='IN', limit=10)

            for playlist in search_results['playlists']['items']:
                playlist_id = playlist['id']
                playlist_name = playlist['name']
                num_songs = playlist['tracks']['total']


                if language_1 == 'odia':
                    language_append = 'odia'
                    pattern = r'\b(?:' + '|'.join(odia_terms) + r')\b'
                elif language_1 == 'malayalam':
                    language_append = 'malayalam'
                    pattern = r'\b(?:' + '|'.join(malayalam_terms) + r')\b'
                elif language_1 == 'gujarati':
                    language_append = 'gujarati'
                    pattern = r'\b(?:' + '|'.join(gujarati_terms) + r')\b'


                
                if re.search(pattern, playlist_name, flags=re.IGNORECASE):
                    playlist_info.append({
                        'PlaylistID': playlist_id,
                        'PlaylistName': playlist_name,
                        'NumSongs': num_songs,
                        
                        'Query': search_query_append,
                        'Language':language_append,
                        'Timestamp': Todays_TimeStamp,
                    })

        # Combine the existing DataFrame with the new data using concat
        new_df = pd.concat([existing_df, pd.DataFrame(playlist_info)], ignore_index=True)

        # Display and save the combined DataFrame to the xlsx file
        #display(new_df)
        new_df.to_excel(xlsx_filename, index=False)

        return new_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



Todays_TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Add Spotify Credentials
spotify_id = '' # (removed for privacy)
spotify_secret = '' #(removed for privacy)

# Create a custom cache handler
cache_path = ".spotify_cache"
cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)

# Create the Spotify client with the custom cache handler
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_id, client_secret=spotify_secret, 
    cache_handler=cache_handler
))


    
def get_main(queries, language):

    if not isinstance(queries, list):
        raise ValueError("Queries must be a list.")

    try:
        playlist_df = get_playlist_id(queries, language)
        print(Todays_TimeStamp, 'Spotify Scrapping Started ')
        print("Successfully Retrieved playlist IDs.\n")
        
    except Exception as e:
        print(f"Error: {str(e)}\n")
        
# To run it in ipynb file  remove comments and then run 


# df_Queries = pd.read_excel("Queries.xlsx")
# queries = df_Queries['Queries'].to_list()
# get_main(queries)







