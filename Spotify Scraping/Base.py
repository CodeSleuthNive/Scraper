#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import main as main


df_Queries = pd.read_excel(r"C:\Users\nivet\Documents\Spotify Scraping\ueries.xlsx")



queries = df_Queries['Queries'].to_list()

try:
    main.get_main(queries)
except Exception as e:
    # Handle and log any exceptions that occur
    print("An error occurred ")
    print(f"Error: {e}")


