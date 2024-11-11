#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import playlist_name_retrieval_main as main


df_Queries = pd.read_excel(r"/home/muzik247/mnt/BACKUP_RUN_BY_MANUAL/Spotify_Playlist_Name_Retrieval/Queries.xlsx")



queries = df_Queries['Queries'].to_list()
language = df_Queries['Language'].to_list()

try:
    main.get_main(queries, language)
except Exception as e:
    # Handle and log any exceptions that occur
    print("An error occurred ")
    print(f"Error: {e}")



