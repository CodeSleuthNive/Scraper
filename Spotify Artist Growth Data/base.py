

import os
import glob
from datetime import datetime
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',50)
import datetime as dt
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
import openpyxl
import Send_mail_text as sms



log_file_path = r"/home/muzik247/mnt/BACKUP_RUN_BY_MANUAL/Spotify_Scrapping_Odia/cron.log"


import re
from datetime import datetime, timedelta


with open(log_file_path, 'r') as log_file:
    log_content = log_file.readlines()

# Define a regular expression pattern to match the date and timestamp
date_pattern = re.compile(r'Date Scrapped: (\d{4}-\d{2}-\d{2})')

# Initialize a flag to track success or failure
success_flag = False

# Initialize variable to store the last extracted date
last_extracted_date = None

# Lines to check without considering numbers inside brackets
required_lines = [
    "retrieving playlists",
    "processing search query",
    "playlist retrieval completed",
    "successfully retrieved playlist ids",
    "extracting playlist details",
    "track occurrence details extraction completed",
    "playlist track details extraction completed",
    "successfully retrieved track ids",
    "extracting audio features",
    "audio features extraction completed",
    "successfully retrieved audio features",
    "processing feature sets",
    "feature clustering completed",
    "successfully retrieved clustered_audio_features",
    "email sent successfully"
]

# Convert required lines to lowercase
required_lines_lower = [line.lower() for line in required_lines]

# Lines to dynamically exclude based on their presence
exclude_lines = [
    "Couldn't read cache at: .cache",
    "Couldn't write token to cache at: .cache",
    "Encountered rate limit or auth error, rotating credentials"
]

# Convert exclude lines to lowercase
exclude_lines_lower = [line.lower() for line in exclude_lines]

for line in log_content:
    date_match = date_pattern.search(line)

    if date_match:
        last_extracted_date = date_match.group(1)
        print('last_extracted_date', last_extracted_date)
        # Check if the required lines are present for the last extracted date
        lines_after_date = log_content[log_content.index(line) + 1:]

        # Remove ellipsis from lines_after_date
        lines_after_date = [log_line.replace('...', '').strip().lower() for log_line in lines_after_date]

        # Exclude lines dynamically based on their presence
        lines_after_date = [log_line for log_line in lines_after_date if not any(exclude_line.lower() in log_line for exclude_line in exclude_lines)]

        # Debugging print statements
        print('Lines after date:', lines_after_date)
        print('Required lines:', required_lines_lower)

        # Check if all required lines are present for the last extracted date
        required_lines_present = all(req_line_lower in lines_after_date for req_line_lower in required_lines_lower)

        # Debugging print statements
        print('Required lines present:', required_lines_present)

        # Check for any lines after the date that are not in the exclude_lines list
        additional_lines_current_iteration = [log_line for log_line in lines_after_date if log_line not in required_lines_lower and log_line not in exclude_lines_lower]

        # Debugging print statements
        print('Additional lines present:', additional_lines_current_iteration)

        # Set success_flag if all required lines are present and no additional lines
        if required_lines_present and not additional_lines_current_iteration:
            success_flag = True

# If all required lines are present and no additional lines for the last extracted date, check if the date is within the current week and the same year as the current date
if success_flag and last_extracted_date:
    extracted_date = datetime.strptime(last_extracted_date, "%Y-%m-%d").date()
    current_date = datetime.now().date()
    start_of_week = current_date - timedelta(days=(current_date.weekday() + 1) % 7)

    if start_of_week <= extracted_date <= current_date:
        Status_to_perform = 'Success'
        print(f"Final Last Extracted Date: {last_extracted_date}")
        print("Success")
    else:
        print("Failed: Date is not within the current week or the same year as the current date")
        Status_to_perform = 'Failed'
else:
    print('Failed: Either required lines are missing or additional lines are present')
    print('Additional lines present:', additional_lines_current_iteration)
    Status_to_perform = 'Failed'



spotify_credentials   = [
    {'client_id': '295235b1359c4b2bb164535cf3e41334', 'client_secret': 'fb94a4e52dbc432bb4d69743d38f90bb'},
     {'client_id': 'e89aaefce0c249b5ad7a963072cbb404', 'client_secret': '9d67e22e93f146ceaf0b60be68ebcc09'},
     {'client_id': '194b3c155d934b74a5403153073c7ecb', 'client_secret': '88b58f756a564dec9f6010d62ae66ebf'},
    {'client_id': '1f894be0f84e45ca8e771ebdaf5d5cae', 'client_secret': '3ead05aaae744e5ca805f56f054cb762'},
    {'client_id': '9f65d1e394124ce8b93c2a2527397ecf', 'client_secret': '6ea20e7b61664bb8b06088bb17af28f3'},
     {'client_id': 'a5eab52b243843c89cef4987052fd854', 'client_secret': '6b1f9c1b9d284d628aea8ac55feddb66'},
     {'client_id': 'f1ab5d195fa74703b8c093c5a613d9e3', 'client_secret': 'd819a80b91b1458c89d1eb4a38c37bcb'},
     
    # Add more keys as needed
]



class SpotifyAPIKeyRotator:
    def __init__(self, credentials):
        self.credentials = credentials
        self.current_index = 0
        self.sp = None
        self.authenticate_spotify()

    def authenticate_spotify(self):
        current_credentials = self.credentials[self.current_index]
        client_credentials_manager = SpotifyClientCredentials(client_id=current_credentials['client_id'],
                                                              client_secret=current_credentials['client_secret'])
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def rotate_credentials(self):
        self.current_index = (self.current_index + 1) % len(self.credentials)
        self.authenticate_spotify()


key_rotator = SpotifyAPIKeyRotator(spotify_credentials)




if Status_to_perform == 'Success':
    print('Status_to_perform', Status_to_perform)
    file_path = r"/home/muzik247/mnt/DEPLOYED_WEB_APPS/Spotify_Report_Data_monitor/Odia/Spotify Report Data Odia.xlsx"

#     file_path = r"\\192.168.2.50\data_analyst\NEW_SERVER\DEPLOYED_WEB_APPS\Spotify_Report_Data_monitor\Odia\Spotify Report Data Odia.xlsx"

    # "\\192.168.2.50\data_analyst\NEW_SERVER\DEPLOYED_WEB_APPS\Spotify_Report_Data_monitor\CG\Spotify_report_data_CG.py"

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file if it doesn't exist
        workbook = openpyxl.Workbook()
        workbook.save(file_path)
        print(f"File created: {file_path}")
    else:
        print(f"File already exists: {file_path}")


    # In[3]:

    directory_path = r'/home/muzik247/mnt/BACKUP_RUN_BY_MANUAL/Spotify_Scrapping_Odia/Clustered_Audio_Features_Data'
#     directory_path = r"\\192.168.2.50\data_analyst\NEW_SERVER\BACKUP_RUN_BY_MANUAL\Spotify_Scrapping\Clustered_Audio_Features_Data"

    # Use glob to get a list of Excel files in the directory
    excel_files = glob.glob(os.path.join(directory_path, '*.xlsx'))

    # Check if there are any Excel files in the directory
    if excel_files:
        # Get the latest modified Excel file
        latest_excel_file = max(excel_files, key=os.path.getmtime)
        
        print("Latest modified Excel file:", latest_excel_file)
    else:
        print("No Excel files found in the specified directory.")


    # In[4]:


    def ordinal(number):
        if 10 <= number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd', 4:'th'}.get(number % 10, 'th')
        return f"{number}{suffix}"

    # Get the current date
    current_date = datetime.now()

    # Calculate the week number of the month
    week_number = (current_date.day - 1) // 7 + 1

    # Get the current year
    current_year = current_date.year

    # Replace 'm_name' with your actual month name
    m_name = current_date.strftime("%B")

    # Get the ordinal form of the week number
    ordinal_week = ordinal(week_number)


    import datetime
    import pandas as pd
    import warnings
    warnings.filterwarnings("ignore")

    current_date1 = datetime.datetime.now().date()
    st_day1=datetime.datetime.now().day
    past_60_dates = [current_date1 - datetime.timedelta(days=i) for i in range(datetime.datetime.now().day)]
    past_60_dates = [x.strftime('%A') for x in  past_60_dates]
    week_num = past_60_dates.count('Monday')
    # week_num
    week_num1 = ordinal(week_num)

    # Create the desired string
    month_name = f'{m_name}_{week_num1}_week_{current_year}'
    # Print the result
    print(month_name)




    # In[5]:


    df_original = pd.read_excel(latest_excel_file)
    # month_name = 'December (2nd week) - 2023'
    new_column = month_name
    df = df_original.copy()


    # In[6]:


    def replace_artist_names(df):
        mapping = {
        'Tarique Aziz': ['Tariq Aziz','Tarique Aziz'],
        'Babushaan Mohanty': ['Babushaan Mohanty','Babushan','Babushan Mohanty'],
        'Abhijit Majumdar': ['Abhijit Majumdar',' Abhijit Majumdhar',' Abhijit Mazumdar'],
        'Abhijit Mishra':[' Abhijit Mishra'],
        'Abhijit Tripathy':[' Abhijit Tripathy',' Abhijit Tirupathy'],
        'Akhyay Mohanty':[' Akhyay Mohanty',' Akshaya Mohanty'],
        'Ananya Sritam Nanda':[' Ananya Sritam Nanda',' Ananya Sriram Nanda',' Ananya Shritam Nanda'],
        'Anuradha Paudwal':[' Anuradha Paudwal',' Anuradha Poudwal'],
        'Papu Pom Pom': ['Papu Pom Pom'],
        'Subhasish Mahakud': ['Subhasish Mahakud','Subhashish'],
        'Jyotirmayee Nayak': ['Jyotirmayee Nayak'],
        'Mohammed Aziz': ['Mohammed Aziz','Md. Aziz'],
        'Kuldeep Pattanaik': ['Kuldeep Pattanaik','Kuldeep', 'Kuldeep Pattnaik','Kuldeep Pattanaik Pattanaik','Kuldeep Pattanaik Pattanaik','Kuldeep Pattanaik Pattnaik'],
        'Humane Sagar': ['Humane Sagar','Humanne Sagar'],
        'Nibedita': ['Nibedita'],
        'Mantu Chhuria': ['Mantu Chhuria','Mantu churia'],
        'Dipti Rekha Padhi': ['Dipti Rekha Padhi', 'Diptirekha Padhi','Diptirekha'],
        'Bijay Anand Sahu': ['Bijay Anand Sahu'],
        'Baidyanath Dash': ['Baidyanath Dash'],
        'Aseema Panda': ['Aseema Panda', 'Ashima Panda','Asima Panda','Asima'],
        'Ipseeta Panda': ['Ipseeta Panda'],
        'Babool Supriyo': ['Babool Supriyo', 'Babul Supriyo'],
        'Arpita Choudhury': ['Arpita Choudhury','Arpita Chowdhury'],
        'Udit Narayan': ['Udit Narayan', 'Udit Naryan'],
        'Pamela Jain': ['Pamela Jain'],
        'Abinash Dash': ['Abinash Dash'],
        'Ananya Sritam Nanda': ['Ananya Sritam Nanda'],
        'Archana Padhi': ['Archana Padhi'],
        'Antara Chakraborty': ['Antara Chakraborty',' Antara Chakrabarty'],
        'Namita Agrawal': ['Namita Agrawal'],
        'Sonu Nigam': ['Sonu Nigam'],
        'Swayam Padhi': ['Swayam Padhi', 'Swayam Padhi Padhi'],
        'Amrita Nayak ':['Amrita Nayak ','AMRITA NAYAK'],
        'Umakant Barik':['UMAKANT BARIK','Umakant Barik' ],
        'Unavailable':['E1']
        }

        for key, values in mapping.items():
            for value in values:
                df['Artists'] = df['Artists'].str.replace(value, key, case=False)

        return df


    # In[7]:


    df_c = df[['Track ID',
        'Artists', 'Occurrences', 'Release_Date', 'features1', 'features2',
        'features3', 'features4', 'features5', 'features6', 'features7',
        'sad_song', 'dance_song', 'valence_high', 'valence_low', 'Timestamp']]


    df_c['Release_Date'] = pd.to_datetime(df_c['Release_Date'],errors = 'coerce') 

    df_c.drop_duplicates(subset=['Track ID'],keep='last',inplace=True)

    df_c['Release_year'] = df_c['Release_Date'].dt.year
    df_c['Release_year'] = df_c['Release_year'].fillna(-1)
    df_c['Release_year'] = df_c['Release_year'].astype(int)

    df_19 = df_c[df_c['Release_year'] == 2019]
    df_20 = df_c[df_c['Release_year'] == 2020]
    df_21 = df_c[df_c['Release_year'] == 2021]
    df_22 = df_c[df_c['Release_year'] == 2022]
    df_23 = df_c[df_c['Release_year'] == 2023]
    df_24 = df_c[df_c['Release_year'] == 2024]


    replace_artist_names(df_19)
    replace_artist_names(df_20)
    replace_artist_names(df_21)
    replace_artist_names(df_22)
    replace_artist_names(df_23)
    replace_artist_names(df_24)
    print('replaced')


    # In[8]:


    df1 = df_c[df_c['Release_year'] >= 2019]

    split_artists = df_19['Artists'].str.split(',', expand=True)
    split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')
    artist_counts_19 = split_artists.value_counts()


    # Convert artist_counts_19 to a set
    artist_set_19 = set(artist_counts_19.index)

    # Convert artist_counts_19 to a dictionary
    artist_dict_19 = artist_counts_19.to_dict()


    split_artists = df_20['Artists'].str.split(',', expand=True)
    split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')
    artist_counts_20 = split_artists.value_counts()
    # Convert artist_counts_20 to a set
    artist_set_20 = set(artist_counts_20.index)

    artist_dict_20 = artist_counts_20.to_dict()


    split_artists = df_21['Artists'].str.split(',', expand=True)
    split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')
    artist_counts_21 = split_artists.value_counts()
    # Convert artist_counts_21 to a set
    artist_set_21 = set(artist_counts_21.index)

    # Convert artist_counts_21 to a dictionary
    artist_dict_21 = artist_counts_21.to_dict()



    split_artists = df_22['Artists'].str.split(',', expand=True)
    split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')
    artist_counts_22 = split_artists.value_counts()
    # Convert artist_counts_22 to a set
    artist_set_22 = set(artist_counts_22.index)

    # Convert artist_counts_22 to a dictionary
    artist_dict_22 = artist_counts_22.to_dict()


    split_artists = df_23['Artists'].str.split(',', expand=True)
    split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')
    artist_counts_23 = split_artists.value_counts()
    # Convert artist_counts_23 to a set
    artist_set_23 = set(artist_counts_23.index)

    # Convert artist_counts_23 to a dictionary
    artist_dict_23 = artist_counts_23.to_dict()


    split_artists = df_24['Artists'].str.split(',', expand=True)
    split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')
    artist_counts_24 = split_artists.value_counts()
    # Convert artist_counts_24 to a set
    artist_set_24 = set(artist_counts_24.index)

    # Convert artist_counts_24 to a dictionary
    artist_dict_24 = artist_counts_24.to_dict()


    common_artist_set = artist_set_24.intersection(artist_set_22,artist_set_21,artist_set_20,artist_set_19,artist_set_23)
    common_artist_set


    # In[9]:


    unique_artists_19 = artist_set_19.difference(artist_set_22, artist_set_21, artist_set_20,artist_set_23, artist_set_24)
    unique_artists_20 = artist_set_20.difference(artist_set_22, artist_set_21, artist_set_19,artist_set_23, artist_set_24)
    unique_artists_21 = artist_set_21.difference(artist_set_22, artist_set_19, artist_set_20,artist_set_23, artist_set_24)
    unique_artists_22 = artist_set_22.difference(artist_set_19, artist_set_21, artist_set_20,artist_set_23, artist_set_24)
    unique_artists_23 = artist_set_23.difference(artist_set_22,artist_set_19, artist_set_21, artist_set_20, artist_set_24)
    unique_artists_24 = artist_set_24.difference(artist_set_22,artist_set_19, artist_set_21, artist_set_20, artist_set_23)


    # In[10]:


    df_top_songs_details = df_original.copy()
    df_top_songs_details.drop_duplicates(subset=['Track ID'],keep='last', inplace=True)
    df_top_songs_details = df_top_songs_details[df_top_songs_details['Occurrences']>=4]
    print('No.of Songs occured more than 4: ',len(df_top_songs_details[['Track ID','Occurrences','Artists']]))
    replace_artist_names(df_top_songs_details)


    # In[11]:


    df = df_original.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Date'] = df['Timestamp'].dt.date

    df  = df[df['Date']==df['Date'].max()]

    print(df.shape)
    df1 = df[['Track ID','Occurrences','Artists']]
    df1.drop_duplicates(subset=['Track ID'],keep='last', inplace=True)
    df1 = df1[df1['Occurrences']>=4]
    # display(df1)
    print(df1.shape)


    # spotify_id = 'a5eab52b243843c89cef4987052fd854' # (removed for privacy)
    # spotify_secret = '6b1f9c1b9d284d628aea8ac55feddb66'



    #changed antipiracy api key
    spotify_id = '9f65d1e394124ce8b93c2a2527397ecf' # (removed for privacy)
    spotify_secret = '6ea20e7b61664bb8b06088bb17af28f3' #(removed for privacy)






    # Create a custom cache handler
    cache_path = ".spotify_cache"
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)

    # Create the Spotify client with the custom cache handler
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=spotify_id, client_secret=spotify_secret,
        cache_handler=cache_handler
    ))

    # Define your list of track IDs
    track_ids = df1['Track ID'].tolist()

    track_details_list = []
    key_rotator = SpotifyAPIKeyRotator(spotify_credentials)

    # Fetch track details for each track ID
    for track_id in track_ids:
        try:
            track_data = key_rotator.sp.track(track_id)
            track_name = track_data['name']
            artists = ', '.join([artist['name'] for artist in track_data['artists']])
            
            # Get the album ID
            album_id = track_data['album']['id']
            
            # Fetch album details
            album_data = key_rotator.sp.album(album_id)
            
            # Extract copyright information from the album
            copyright_info = album_data['copyrights']
            
            track_details_list.append({
                'Track ID': track_id,
                'Track Name': track_name,
                'Artists': artists,
                'Copyright Information': copyright_info
            })
        except spotipy.SpotifyException as e:
            print(f"Failed to fetch data for track ID: {track_id}")
            print(f"Error: {e}")

    # Convert the list of track details into a Pandas DataFrame
    track_details_df = pd.DataFrame(track_details_list)


    from datetime import datetime
    from datetime import date
    def extract_publisher_name(row):
        try:
            first_copyright = row[0]['text']
            
            # Remove any leading copyright symbol (©)
            cleaned_copyright = first_copyright.lstrip('©').strip()
            
            # Remove all numbers from the text
            publisher_name = re.sub(r'\d', '', cleaned_copyright)
            
            # Check if the result is not empty and contains at least one alphanumeric character
            if publisher_name.strip() and any(c.isalnum() for c in publisher_name):
                return publisher_name.strip()  # Remove leading/trailing whitespace
            else:
                return None
        except (IndexError, TypeError):
            return None


    # Apply the function to create a new column 'Publisher Name' in the DataFrame
    track_details_df['Publisher Name'] = track_details_df['Copyright Information'].apply(extract_publisher_name)


    track_details_df1 = track_details_df[['Track ID','Track Name','Publisher Name']]
    report_df = track_details_df1.merge(df1[['Track ID','Occurrences','Artists']], on ='Track ID', how='outer')
    report_df = report_df[['Track ID','Track Name','Occurrences','Artists','Publisher Name']]
    report_df['Timestamp'] =  date.today()

    report_df.drop_duplicates(subset=['Track ID'], inplace=True)
    report_df = report_df[report_df['Occurrences']>=4]
    report_df.rename(columns={'Track ID':'Track_ID'}, inplace=True)


    # In[ ]:





    # In[12]:


    def top_song_artists(df_name, year):
        # Split the 'Artists' column by comma
        split_artists = df_name['Artists'].str.split(',', expand=True)

        # Reshape the split_artists DataFrame to a Series
        split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')

        # Perform value_counts() on the individual artists
        artist_counts = split_artists.value_counts()

        filtered_counts = artist_counts[(artist_counts >= 1)]

        # Create a dictionary to store artist names and their counts
        artist_dict = dict(filtered_counts)

        # Sort the dictionary items alphabetically by artist name
        sorted_artist_dict = dict(sorted(artist_dict.items()))

        # Return the sorted dictionary
        return sorted_artist_dict


    def clean_name(name):
        if isinstance(name, str):
            return name.strip().lower()
        else:
            # Handle the case where name is not a string (e.g., if it's a float)
            return name
        
        
        
    def excel_sheet_creation(file_path,sheet_name):
        try:
            excel_names = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Sheet '{sheet_name}' exists.")
            reindex_column = 'No'
            
            
        except FileNotFoundError:
            print(f"File not found: {file_path}. Creating it...")

            # Create the Excel file with the specified sheet
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                pd.DataFrame().to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"File and sheet '{sheet_name}' created.")
            reindex_column = 'Yes'
            
            
        except:
            print(f"Sheet '{sheet_name}' not found. Creating it...")

            # Create the sheet in the existing Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
                writer.book.create_sheet(sheet_name)
                pd.DataFrame().to_excel(writer, sheet_name=sheet_name, index=False)

            print(f"Sheet '{sheet_name}' created in the existing Excel file.")
            reindex_column = 'Yes'

            
        return file_path, sheet_name, reindex_column
            
        
        


    def reindexing_column(df_excel, target_column, sheet_name):
        
        if sheet_name == 'artist_top':
            columns_order = target_column + [col for col in df_excel.columns if col not in target_column]
            order_output = df_excel[columns_order].copy()  # Create a new DataFrame with the desired column order
            return order_output
        
        
    def multiple_reindexing_column(all_dfs,target_columns):
        
    #     target_columns = ['Track_ID', 'Track Name', 'Artists', 'Publisher Name']

        # Iterate over each sheet in the dictionary
        for sheet_name, df_excel in all_dfs.items():
            # Check if all target columns are in the DataFrame columns
            if all(col in df_excel.columns for col in target_columns):
                # Reorder the columns to have the target columns at the beginning
                columns_order = target_columns + [col for col in df_excel.columns if col not in target_columns]
                all_dfs[sheet_name] = df_excel[columns_order]

                multi_order_output = all_dfs[sheet_name]
                
        return multi_order_output

        
                    
    def write_excel_sheet2(all_dfs,sheet_name):
        

        
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                all_dfs.to_excel(writer, sheet_name=sheet_name, index=False)

                print("Script executed successfully.")

                    

        
        
    def read_excel(file_path, sheet_name):
        # Function to clean and normalize artist names
        all_dfs = pd.read_excel(file_path, sheet_name=None)
        df_excel = all_dfs[sheet_name]
        
        all_dfs_output = all_dfs
        
        return all_dfs_output, df_excel



        

    def specific_final_code(df_excel, program_results, program_results_clean, program_names,sheet_name, all_dfs):
        
        if sheet_name == 'artist_top':

            if 'Artist_Name' in df_excel.columns:
            
                excel_names_artist = set(df_excel['Artist_Name'])
                new_artists = program_names - excel_names_artist


                df_excel['Clean_Artist_Name'] = df_excel['Artist_Name'].apply(clean_name)
                df_excel[new_column] = 0  
                new_artists_clean = set(program_results_clean.keys()) -  set(df_excel['Clean_Artist_Name'])
                df_excel.loc[~df_excel['Clean_Artist_Name'].isin(new_artists_clean), new_column] += df_excel['Clean_Artist_Name'].map(lambda x: program_results_clean.get(x, 0))

            else:
                new_artists_clean = set(program_results_clean.keys())
                if new_column not in df_excel.columns:
                    df_excel[new_column] = 0  
                    


            

            df_new_artists = pd.DataFrame(program_results.items(), columns=['Artist_Name', new_column])
            df_new_artists = df_new_artists[df_new_artists['Artist_Name'].apply(clean_name).isin(new_artists_clean)]


            if 'Clean_Artist_Name' in df_excel.columns:
                df_excel.drop(columns=['Clean_Artist_Name'], inplace=True)

            all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
            
            output = all_dfs[sheet_name]
            

        
        
        elif sheet_name == 'top_song_details':
            
            print('step1')
            
            if 'Track_ID' in df_excel.columns:
        
                df_excel['Clean_Track_ID'] = df_excel['Track_ID']
                df_excel[new_column] = 0 
                new_artists_clean = set(program_results_clean.keys()) - set(df_excel['Clean_Track_ID'])
                df_excel.loc[~df_excel['Clean_Track_ID'].isin(new_artists_clean), new_column] += df_excel['Clean_Track_ID'].map(lambda x: program_results_clean.get(x, 0))


            else:
                new_artists_clean = set(program_results_clean.keys())
                if new_column not in df_excel.columns:
                    df_excel[new_column] = 0 
                

            
            # Create a DataFrame for the newly added artists and their values
            df_new_artists = pd.DataFrame(program_results.items(), columns=['Track_ID', new_column])
            
  

            # Filter the new artists based on the identified set
            df_new_artists1 = df_new_artists[df_new_artists['Track_ID'].isin(new_artists_clean)]

    #         display(df_new_artists1)
            df_new_artists = pd.merge(report_df, df_new_artists1, on='Track_ID')
    #         display(df_new_artists)

            df_new_artists = df_new_artists[['Track_ID','Track Name','Artists','Publisher Name',new_column]]

            # Drop the temporary cleaned column

            if 'Clean_Track_ID' in df_excel:
                df_excel.drop(columns=['Clean_Track_ID'], inplace=True)

            # Append the DataFrame for the newly added artists to the existing Excel file
            all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
            
            output = all_dfs[sheet_name]
            
            
            
            
        elif sheet_name == 'Music Label Occurence':
            
            if 'Publisher' in df_excel.columns:
                df_excel['Clean_Publisher'] = df_excel['Publisher'].apply(clean_name)
                df_excel[new_column] = 0 

                new_artists_clean = set(program_results_clean.keys()) - set(df_excel['Clean_Publisher'])

                df_excel.loc[~df_excel['Clean_Publisher'].isin(new_artists_clean), new_column] += df_excel['Clean_Publisher'].map(lambda x: program_results_clean.get(x, 0))


            else:

                new_artists_clean = set(program_results_clean.keys())

                if new_column not in df_excel.columns:
                    df_excel[new_column] = 0    



            # Create a DataFrame for the newly added artists and their values
            df_new_artists = pd.DataFrame(program_results.items(), columns=['Publisher', new_column])

            # Filter the new artists based on the identified set
            df_new_artists = df_new_artists[df_new_artists['Publisher'].apply(clean_name).isin(new_artists_clean)]

            if 'Clean_Publisher' in df_excel.columns:
            # Drop the temporary cleaned column
                df_excel.drop(columns=['Clean_Publisher'], inplace=True)

            # Append the DataFrame for the newly added artists to the existing Excel file
            all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
            
            output = all_dfs[sheet_name]
                
            
        elif sheet_name ==  "Artist Growth from 2019":
            
            if 'Artist_Name' in df_excel.columns:
                df_excel_artist = set(df_excel['Artist_Name'])
                new_artists = set(program_results.keys()) - set(df_excel['Artist_Name'])
                df_excel['Clean_Artist_Name'] = df_excel['Artist_Name'].apply(clean_name)

                df_excel[new_column] = 0 
                print(df_excel.columns)# If not, create it with initial values as 0

                # Identify new artists by comparing cleaned names
                new_artists_clean = set(program_results_clean.keys()) - set(df_excel['Clean_Artist_Name'])

                # Update the new column for existing artists
                df_excel.loc[~df_excel['Clean_Artist_Name'].isin(new_artists_clean), new_column] += df_excel['Clean_Artist_Name'].map(lambda x: program_results_clean.get(x, 0))


            else:
                new_artists = program_names
                new_artists_clean = set(program_results_clean.keys())
                if new_column not in df_excel.columns:
                    df_excel[new_column] = 0 


            

            # Create a DataFrame for the newly added artists and their values
            df_new_artists = pd.DataFrame(program_results.items(), columns=['Artist_Name', new_column])

            # Filter the new artists based on the identified set
            df_new_artists = df_new_artists[df_new_artists['Artist_Name'].apply(clean_name).isin(new_artists_clean)]


            if 'Clean_Artist_Name' in df_excel.columns:
            # Drop the temporary cleaned column
                df_excel.drop(columns=['Clean_Artist_Name'], inplace=True)

            # Append the DataFrame for the newly added artists to the existing Excel file
            all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
            
            output = all_dfs[sheet_name]

            
            
        elif sheet_name =='"Unique Artists Growth"':
            
            
            if 'Artist_Name' in df_excel.columns:
                df_excel_artist = set(df_excel['Artist_Name'])
                new_artists = set(program_results.keys()) - set(df_excel['Artist_Name'])
                df_excel['Clean_Artist_Name'] = df_excel['Artist_Name'].apply(clean_name)

                df_excel[new_column] = 0 
    #             print(df_excel.columns)# If not, create it with initial values as 0

                # Identify new artists by comparing cleaned names
                new_artists_clean = set(program_results_clean.keys()) - set(df_excel['Clean_Artist_Name'])

                # Update the new column for existing artists
                df_excel.loc[~df_excel['Clean_Artist_Name'].isin(new_artists_clean), new_column] += df_excel['Clean_Artist_Name'].map(lambda x: program_results_clean.get(x, 0))


            else:
                new_artists = program_names
                new_artists_clean = set(program_results_clean.keys())
                
                if new_column not in df_excel.columns:
                    df_excel[new_column] = 0 


            

            # Create a DataFrame for the newly added artists and their values
            df_new_artists = pd.DataFrame(program_results.items(), columns=['Artist_Name', new_column])

            # Filter the new artists based on the identified set
            df_new_artists = df_new_artists[df_new_artists['Artist_Name'].apply(clean_name).isin(new_artists_clean)]


            if 'Clean_Artist_Name' in df_excel.columns:
            # Drop the temporary cleaned column
                df_excel.drop(columns=['Clean_Artist_Name'], inplace=True)

            # Append the DataFrame for the newly added artists to the existing Excel file
            all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
            
            output = all_dfs[sheet_name]
            
        return output
            




    # In[13]:


    def artist_top_excel_writer(file_path):
        
        result_dict_top_song_details = top_song_artists(df_top_songs_details, 'top songs')
        program_names = set(result_dict_top_song_details.keys())
        program_results = result_dict_top_song_details
        program_results_clean = {clean_name(key): value for key, value in program_results.items()}
        
        
        sheet_name = "artist_top"
        file_path, sheet_name, reindex_column = excel_sheet_creation(file_path,sheet_name)
        all_dfs, df_excel = read_excel(file_path,sheet_name)
        
    
    #     new_artists = specific_code(df_excel, sheet_name, program_names)
        output = specific_final_code(df_excel, program_results, program_results_clean, program_names, sheet_name, all_dfs)
        
        
        if reindex_column == 'Yes':
            target_column = ['Artist_Name']
            order_output = reindexing_column(output, target_column,sheet_name)
        else:
            order_output = output 
            
    #     overall_output = write_excel_sheet2(order_output,sheet_name)    
        
        return order_output





    def top_song_details_excel_writer(file_path):
        track_occurrences_dict = dict(zip(report_df['Track_ID'], report_df['Occurrences']))
        program_results = track_occurrences_dict
        sheet_name = 'top_song_details'
        target_columns = ['Track_ID', 'Track Name', 'Artists', 'Publisher Name']
        file_path, sheet_name, reindex_column = excel_sheet_creation(file_path,sheet_name)
        all_dfs, df_excel = read_excel(file_path,sheet_name)
        program_results = track_occurrences_dict
        program_results_clean = {key: value for key, value in program_results.items()}
        output = specific_final_code(df_excel, program_results, program_results_clean,{}, sheet_name, all_dfs)
        
        
        if reindex_column == 'Yes':
            target_columns = ['Track_ID', 'Track Name', 'Artists', 'Publisher Name']
            multi_reindexed = multiple_reindexing_column(all_dfs,target_columns)
        else:
            multi_reindexed = output 
        
        
    #     overall_output = write_excel_sheet2(multi_reindexed,sheet_name) 
        
        return multi_reindexed
        


    # In[15]:


    def music_label_occurence(file_path):
        
        value_counts_dict = report_df['Publisher Name'].value_counts().to_dict()
        program_results = value_counts_dict

        sheet_name = 'Music Label Occurence'
        target_columns = ['Publisher']

        file_path, sheet_name, reindex_column = excel_sheet_creation(file_path,sheet_name)
        all_dfs, df_excel = read_excel(file_path,sheet_name)

        program_results_clean = {clean_name(key): value for key, value in program_results.items()}
        program_results_clean = {key.strip().replace('  ', ' '): value for key, value in program_results_clean.items()}
        output = specific_final_code(df_excel, program_results, program_results_clean,{}, sheet_name, all_dfs)
        
        
        if reindex_column == 'Yes':
            target_columns = ['Publisher']
            multi_reindexed = multiple_reindexing_column(all_dfs,target_columns )
        else:
            multi_reindexed = output 
        
        
        return multi_reindexed





    def year_wise_artist_artist_growth_2019(df_name, year):
        # Split the 'Artists' column by comma
        split_artists = df_name['Artists'].str.split(',', expand=True)

        # Reshape the split_artists DataFrame to a Series
        split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')

        # Perform value_counts() on the individual artists
        artist_counts = split_artists.value_counts()

        filtered_counts = artist_counts[(artist_counts >= 5)]

        # Create a dictionary to store artist names and their counts
        artist_dict = dict(filtered_counts)

        # Sort the dictionary items alphabetically by artist name
        sorted_artist_dict = dict(sorted(artist_dict.items()))

        # Return the sorted dictionary
        return sorted_artist_dict




    def artist_growth_2019_excel_writer(df_c,file_path ):
        
        df1 = df_c[df_c['Release_year'] >= 2019]
        df1 = replace_artist_names(df1)
        result_dict_from_2019 = year_wise_artist_artist_growth_2019(df1, 'artist growth ')
        sheet_name = "Artist Growth from 2019"
        file_path, sheet_name, reindex_column = excel_sheet_creation(file_path,sheet_name)
        all_dfs, df_excel = read_excel(file_path,sheet_name)
        
        program_names = set(result_dict_from_2019.keys())
        program_results = result_dict_from_2019
        
        

        program_results_clean = {clean_name(key): value for key, value in program_results.items()}
        target_columns = ['Artist_Name']
        output = specific_final_code(df_excel, program_results, program_results_clean,program_names, sheet_name, all_dfs)
        # display(all_dfs.items())
        
        if reindex_column == 'Yes':
            target_columns = ['Artist_Name']

            for sheet_name, df_excel in all_dfs.items():
                # Check if all target columns are in the DataFrame columns
                if all(col in df_excel.columns for col in target_columns):
                    # Reorder the columns to have the target columns at the beginning
                    columns_order = target_columns + [col for col in df_excel.columns if col not in target_columns]
                    all_dfs[sheet_name] = df_excel[columns_order]
                    multi_reindexed = all_dfs[sheet_name]
                    # display(multi_reindexed)
        

        else:
            multi_reindexed = output 
    #     multi_reindexed = multiple_reindexing_column(output,target_columns )
        
    #     display(multi_reindexed)
        
        return multi_reindexed





    def excel_appender(unique_artist_dict,artist_dict_name,unique_artists_name, year,file_path):
        sheet_name = "Unique Artists Growth"
        
        
        file_path, sheet_name, reindex_column = excel_sheet_creation(file_path,sheet_name)
        all_dfs, df_excel = read_excel(file_path,sheet_name)
        
        
        program_names = set(unique_artist_dict.keys())
        
        if 'Artist_Name' in df_excel.columns:
            
            excel_names_artist = set(df_excel['Artist_Name'])
            new_artists = program_names - excel_names_artist
    

        else:
            new_artists = program_names

        # Print the list of newly added artists
        print("Newly Added Artists:")
        for artist in new_artists:
            print(artist)


        program_results = unique_artist_dict
        program_results_clean = {clean_name(key): value for key, value in program_results.items()}

    
        
        if 'Artist_Name' in df_excel.columns:
            df_excel['Clean_Artist_Name'] = df_excel['Artist_Name'].apply(clean_name)
            
            if new_column not in df_excel.columns:
                df_excel[new_column] = 0
            # If not, create it with initial values as 0

            new_artists_clean = set(program_results_clean.keys()) - set(df_excel['Clean_Artist_Name'])
            condition = ~df_excel['Clean_Artist_Name'].isin(new_artists_clean) & (df_excel['Song_Released_Year'] == year)

            # Update the specified column based on the condition
            df_excel.loc[condition, new_column] += df_excel.loc[condition, 'Clean_Artist_Name'].map(lambda x: program_results_clean.get(x, 0))

        else:
            
            new_artists_clean = set(program_results_clean.keys())
            
            if new_column not in df_excel.columns:
                df_excel[new_column] = 0
        
        
        # Create a DataFrame for the newly added artists and their values
        df_new_artists = pd.DataFrame(program_results.items(), columns=['Artist_Name', new_column])

        # Filter the new artists based on the identified set
        df_new_artists = df_new_artists[df_new_artists['Artist_Name'].apply(clean_name).isin(new_artists_clean)]
        df_new_artists['Song_Released_Year'] = year
        
        
        
        if 'Clean_Artist_Name' in df_excel.columns:

        # Drop the temporary cleaned column
            df_excel.drop(columns=['Clean_Artist_Name'], inplace=True)

        # Append the DataFrame for the newly added artists to the existing Excel file
        all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
        
        
        
        if reindex_column == 'Yes':
        
        
            target_columns = ['Artist_Name', 'Song_Released_Year']

            # Iterate over each sheet in the dictionary
            for sheet_name, df_excel in all_dfs.items():
                # Check if all target columns are in the DataFrame columns
                if all(col in df_excel.columns for col in target_columns):
                    # Reorder the columns to have the target columns at the beginning
                    columns_order = target_columns + [col for col in df_excel.columns if col not in target_columns]
                    all_dfs[sheet_name] = df_excel[columns_order]
                    ordered_output = all_dfs[sheet_name]
                    
                    
        else:
            
            ordered_output = all_dfs[sheet_name]
            
            



        # Save the updated DataFrames back to the Excel file
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet, df in all_dfs.items():
                df.to_excel(writer, sheet_name=sheet, index=False)

        print("Script executed successfully.")
        print('\n')
    

        return ordered_output
        

    def unique_artist_appender(artist_dict_name,unique_artists_name, year, file_path):
        
        
        unique_artist_counts = {artist: artist_dict_name.get(artist, 0) for artist in unique_artists_name}

        # Sort the unique_artist_counts dictionary by values in descending order
        unique_artist_dict = dict(sorted(unique_artist_counts.items(), key=lambda item: item[1], reverse=True))
        
        output = excel_appender(unique_artist_dict,artist_dict_name,unique_artists_name, year, file_path)
        
        print('*******************************************************')

        return output



    unique_artist_appender_b1 = unique_artist_appender(artist_dict_19, unique_artists_19,2019, file_path)
    unique_artist_appender_b2 = unique_artist_appender(artist_dict_20, unique_artists_20,2020,file_path)
    unique_artist_appender_b3 = unique_artist_appender(artist_dict_21, unique_artists_21,2021, file_path)
    unique_artist_appender_b4 = unique_artist_appender(artist_dict_22, unique_artists_22,2022, file_path)
    unique_artist_appender_b5 = unique_artist_appender(artist_dict_23, unique_artists_23,2023, file_path)
    unique_artist_appender_b6 = unique_artist_appender(artist_dict_24, unique_artists_24,2024, file_path)
        


    # In[22]:


    def indiviual_year_wise_artist(df_name, year, file_path):
        # Split the 'Artists' column by comma
        split_artists = df_name['Artists'].str.split(',', expand=True)

        # Reshape the split_artists DataFrame to a Series
        split_artists = split_artists.stack().str.strip().reset_index(level=1, drop=True).rename('Artist')

        # Perform value_counts() on the individual artists
        artist_counts = split_artists.value_counts()
        
        print(artist_counts)
        


        current_year = datetime.now().year
        
        if year !=current_year:

            filtered_counts = artist_counts[(artist_counts >= 2)]
            
        else:
            filtered_counts = artist_counts[(artist_counts >= 1)]
            

        # Create a dictionary to store artist names and their counts
        artist_dict = dict(filtered_counts)

        # Sort the dictionary items alphabetically by artist name
        result_dict = dict(sorted(artist_dict.items()))

    

        sheet_name = "individual year artist growth"
        
        file_path, sheet_name, reindex_column = excel_sheet_creation(file_path,sheet_name)
        all_dfs, df_excel = read_excel(file_path,sheet_name)

        
        
        program_names = set(result_dict.keys())
        program_results = result_dict
        program_results_clean = {clean_name(key): value for key, value in program_results.items()}
        
        if 'Artist_Name' in df_excel.columns:
        
            excel_names_artist = set(df_excel['Artist_Name'])
            new_artists = program_names - excel_names_artist
            df_excel['Clean_Artist_Name'] = df_excel['Artist_Name'].apply(clean_name)
            
            if new_column not in df_excel.columns:
                df_excel[new_column] = 0  # If not, create it with initial values as 0

            # Identify new artists by comparing cleaned names
            new_artists_clean = set(program_results_clean.keys()) - set(df_excel['Clean_Artist_Name'])

            # Update the new column for existing artists
        #     df_excel.loc[~df_excel['Clean_Artist_Name'].isin(new_artists_clean), new_column] += df_excel['Clean_Artist_Name'].map(lambda x: program_results_clean.get(x, 0))
            condition = ~df_excel['Clean_Artist_Name'].isin(new_artists_clean) & (df_excel['Year'] == year)

        # Update the specified column based on the condition
            df_excel.loc[condition, new_column] += df_excel.loc[condition, 'Clean_Artist_Name'].map(lambda x: program_results_clean.get(x, 0))

            
            
        else:
            
            new_artists_clean = set(program_results_clean.keys())


        df_new_artists = pd.DataFrame(program_results.items(), columns=['Artist_Name', new_column])

        # Filter the new artists based on the identified set
        df_new_artists = df_new_artists[df_new_artists['Artist_Name'].apply(clean_name).isin(new_artists_clean)]
    #     df_new_artists['Year'] = np.where(df_new_artists['Artist_Name'].isin(new_artists_clean), year, np.nan)


        df_new_artists['Year'] = year
        # Drop the temporary cleaned column
        
        if 'Clean_Artist_Name' in df_excel.columns:
        
            df_excel.drop(columns=['Clean_Artist_Name'], inplace=True)


        # Append the DataFrame for the newly added artists to the existing Excel file
        all_dfs[sheet_name] = pd.concat([df_excel, df_new_artists], ignore_index=True)
        
        
        
        if reindex_column == 'Yes':
            target_columns = ['Artist_Name', 'Year']
                
            # Iterate over each sheet in the dictionary
            for sheet_name, df_excel in all_dfs.items():
                # Check if all target columns are in the DataFrame columns
                if all(col in df_excel.columns for col in target_columns):
                    # Reorder the columns to have the target columns at the beginning
                    columns_order = target_columns + [col for col in df_excel.columns if col not in target_columns]
                    all_dfs[sheet_name] = df_excel[columns_order]
                    
                    ordered_output = all_dfs[sheet_name]
        else:
            ordered_output = all_dfs[sheet_name]
        
        

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for sheet, df in all_dfs.items():
                df.to_excel(writer, sheet_name=sheet, index=False)

        print("Script executed successfully.")
        
        
        return ordered_output
        
        


    # In[23]:


    indiviual_year_wise_artist_a1 = indiviual_year_wise_artist(df_19,2019, file_path)
    indiviual_year_wise_artist_a2= indiviual_year_wise_artist(df_20,2020, file_path)
    indiviual_year_wise_artist_a3 = indiviual_year_wise_artist(df_21,2021, file_path)
    indiviual_year_wise_artist_a4 = indiviual_year_wise_artist(df_22,2022, file_path)
    indiviual_year_wise_artist_a5 = indiviual_year_wise_artist(df_23,2023, file_path)
    indiviual_year_wise_artist_a6 = indiviual_year_wise_artist(df_24,2024, file_path)


    # In[24]:


    artist_top_df = artist_top_excel_writer(file_path)
    top_song_details_df =  top_song_details_excel_writer(file_path)
    Music_Label_Occurence_df = music_label_occurence(file_path)
    Artist_Growth_from_2019_df = artist_growth_2019_excel_writer(df_c,file_path )


    # In[25]:


    dfs = [artist_top_df, top_song_details_df, Music_Label_Occurence_df, Artist_Growth_from_2019_df, unique_artist_appender_b5, indiviual_year_wise_artist_a5]

    # List of corresponding sheet names
    sheet_names = ['artist_top', 'top_song_details', 'Music Label Occurence', 'Artist Growth from 2019','Unique Artists Growth', 'individual year artist growth' ]

    # Excel file path
    excel_file_path = file_path

    # Save each DataFrame to the corresponding sheet in the Excel file
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        for sheet, df in zip(sheet_names, dfs):
            df.to_excel(writer, sheet_name=sheet, index=False)

    print("DataFrames saved to Excel file successfully.")


    subject = 'Odia Spotify Scrapping File Writing Process Success'
    output = "I'm pleased to confirm the successful extraction of Spotify details, now integrated into our master file."
    
    sender_email = 'nivetha@tapmobi.in'
    sender_password = 'Tapmobi@07'
    recipient_emails = ['datateam@tapmobi.in','nivetha@tapmobi.in']

# Send email notification
    sms.send_mail_alert(subject, output, sender_email, sender_password, recipient_emails)


elif Status_to_perform == 'Failed':
    print('Status_to_perform', Status_to_perform)
    subject = 'Odia Spotify Scrapping File Writing Process Failed'
    output = "Regrettably, the Spotify data extraction process encountered issues."
    
    sender_email = 'nivetha@tapmobi.in'
    sender_password = 'Tapmobi@07'
    recipient_emails = ['datateam@tapmobi.in','nivetha@tapmobi.in']

# Send email notification
    sms.send_mail_alert(subject, output, sender_email, sender_password, recipient_emails)


else:
    print('Status_to_perform', Status_to_perform)
 
    subject = 'Odia Spotify Scrapping File Writing Process Unknownly Failed'
    output = "Regrettably, the Spotify data extraction process encountered issues."
    
    sender_email = 'nivetha@tapmobi.in'
    sender_password = 'Tapmobi@07'
    recipient_emails = ['datateam@tapmobi.in','nivetha@tapmobi.in']

# Send email notification
    sms.send_mail_alert(subject, output, sender_email, sender_password, recipient_emails)

