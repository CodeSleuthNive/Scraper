import os
import time
import spotipy
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import re
from spotipy.oauth2 import SpotifyClientCredentials
import Send_mail_text as sms

import warnings
warnings.filterwarnings("ignore")


from datetime import date
from datetime import timedelta
import traceback

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import sys


# Replace these with your own Spotify API keys
spotify_credentials   = [
     {'client_id': '', 'client_secret': ''},
     {'client_id': '', 'client_secret': ''},
   
    
     
    # Add more keys as needed
]


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPIKeyRotator:
    def __init__(self, credentials):
        self.credentials = credentials
        self.current_index = 0
        self.sp = None
        self.authenticate_spotify()

    def authenticate_spotify(self):
        current_credentials = self.credentials[self.current_index]
        print('\n\n\n id',current_credentials['client_id'])
        print('secret', current_credentials['client_secret'])
        print('\n\n\n')
        
        client_credentials_manager = SpotifyClientCredentials(client_id=current_credentials['client_id'],
                                                              client_secret=current_credentials['client_secret'])
        
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
    
    def rotate_credentials(self):
        self.current_index = (self.current_index + 1) % len(self.credentials)
        self.authenticate_spotify()



from datetime import datetime
# Get the current year
current_year = date.today().year


def print_bold(message):
    """Prints a message in bold format."""
    print(f"{message}")

def Find_last_Csv(pat):
    directory_path = pat
    try:
        # Get the list of files in the directory with modification dates
        files = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".xlsx"):  # Filter only CSV files
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    modification_date = os.path.getmtime(file_path)
                    files.append((file_path, modification_date))

        # Sort the files based on modification dates in descending order
        sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
        if len(sorted_files) > 0:
            latest_file_path = sorted_files[0][0]
            modification_date = sorted_files[0][1]

            # Convert modification timestamp to a human-readable date
            #modification_date = datetime.fromtimestamp(modification_date).strftime('%d-%m-%Y')

            modification_date = datetime.datetime.fromtimestamp(modification_date)
            modification_date = modification_date.strftime('%d-%m-%Y')

        else:
            print("No files found in the directory")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()

    return latest_file_path

def cluster_features(audio_features):
    """
    Perform feature clustering on the given DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing the features.

    Returns:
        pd.DataFrame: DataFrame with additional columns representing the clusters.

    Raises:
        ValueError: If the input DataFrame is empty or contains missing values.
    """

    for column in audio_features.columns:
    # Check if the column has string data type
        if audio_features[column].dtype == 'O':
            # Fill null values in string columns with 'unavailable'
            audio_features[column] = audio_features[column].fillna('unavailable')


    if audio_features.empty:
        raise ValueError("Input DataFrame is empty.")

    if audio_features.isnull().values.any():
        raise ValueError("Input DataFrame contains missing values.")

    Clustered_Audio_Features = audio_features.copy()

    # Define the feature sets
    features1 = ['Loudness', 'Energy', 'Valence', 'Instrumentalness']
    features2 = ['Acousticness', 'Instrumentalness']
    features3 = ['Speechiness', 'Valence', 'Instrumentalness', 'Energy']
    features4 = ['Valence', 'Energy', 'Speechiness']
    features5 = ['Loudness', 'Energy', 'Valence']
    features6 = ['Acousticness']
    features7 = ['Speechiness', 'Valence', 'Energy']
    sad_song = ['Valence', 'Tempo', 'Energy', 'Mode', 'Acousticness', 'Instrumentalness']
    dance_song = ['Tempo', 'Energy', 'Valence', 'Danceability']
    valence_high = ['Speechiness', 'Energy', 'Valence', 'Danceability']
    valence_low = ['Acousticness', 'Loudness', 'Tempo', 'Valence']

    # Create a list of feature sets
    feature_sets = [features1, features2, features3, features4, features5, features6, features7, sad_song, dance_song, valence_high, valence_low]
    
    print_bold("Processing Feature Sets")
    # Iterate over each set of features
    for i, features in enumerate(feature_sets):
        df_subset = Clustered_Audio_Features[features]
        
        # Apply Min-Max scaling to normalize the data
        scaler = MinMaxScaler()
        normalized_data = scaler.fit_transform(df_subset)
        normalized_data = pd.DataFrame(normalized_data, columns=df_subset.columns)
        
        # Find the optimal number of clusters using the elbow method
        inertia = []
        k_values = range(1, 11)
        
        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=0)
            kmeans.fit(normalized_data)
            inertia.append(kmeans.inertia_)
        
        elbow_index = 2  # Update this with the index of the elbow value you identified
        num_clusters = elbow_index + 1
        
        # Create a K-means model with the specified number of clusters
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(normalized_data)
        cluster_labels = kmeans.labels_
        
        # Add the cluster labels to the original dataframe with a column name based on the feature set
        cluster_column_name = f"Cluster_{i+1}"
        Clustered_Audio_Features[cluster_column_name] = cluster_labels
    
    # Define the current column names and the new column names
    current_columns = ['Cluster_1', 'Cluster_2', 'Cluster_3', 'Cluster_4', 'Cluster_5', 'Cluster_6', 'Cluster_7', 'Cluster_8', 'Cluster_9', 'Cluster_10', 'Cluster_11']
    new_columns = ['features1', 'features2', 'features3', 'features4', 'features5', 'features6', 'features7', 'sad_song', 'dance_song', 'valence_high', 'valence_low']
    
    # Use the rename() method to rename the columns
    Clustered_Audio_Features.rename(columns=dict(zip(current_columns, new_columns)), inplace=True)
    
    # Create a new column with the current date and time
    Clustered_Audio_Features['Timestamp'] = datetime.datetime.now()
    


    print("Feature clustering completed")
    
    Clustered_Audio_Features_path =  r"C:\Users\nivet\Documents\Spotify Scraping\Clustered_Audio_Features_Data"
    # Moutname_Track = f'Clustered_Audio_Features ' + str(Todays_TimeStamp.strftime("%B")) +'_{current_year}'+' data.xlsx'
    Moutname_Track =  f'Clustered_Audio_Features {Todays_TimeStamp.strftime("%B")}_{current_year} data.xlsx'




    MfullPathname_Clustered_Audio_Features = os.path.join(Clustered_Audio_Features_path, Moutname_Track)

    if os.path.exists(Clustered_Audio_Features_path):
        if os.path.exists(MfullPathname_Clustered_Audio_Features):
            existing_data = pd.read_excel(MfullPathname_Clustered_Audio_Features)
            #new_cluster_audio_features = Clustered_Audio_Features[~Clustered_Audio_Features['Track ID'].isin(existing_data['Track ID'])]
            updated_data = pd.concat([existing_data, Clustered_Audio_Features], ignore_index=True)
            updated_data.to_excel(MfullPathname_Clustered_Audio_Features, index=False)
        else:
            Clustered_Audio_Features.to_excel(MfullPathname_Clustered_Audio_Features, index=False)

    else:
        os.makedirs(Clustered_Audio_Features_path)
        Clustered_Audio_Features.to_excel(MfullPathname_Clustered_Audio_Features, index=False)

    return Clustered_Audio_Features


def replace_artist_names(audio_features):
    mapping = {
    'Tariq Aziz': ['Tariq Aziz','Tarique Aziz',],
    'Babushaan Mohanty': ['Babushaan Mohanty','Babushan', 'Babushaan Mohanty','Babushan Mohanty'],
    'Abhijit Majumdar': ['Abhijit Majumdar',' Abhijit Majumdhar',' Abhijit Mazumdar'],
    'Abhijit Mishra':[' Abhijit Mishra'],
    'Abhijit Tripathy':[' Abhijit Tripathy',' Abhijit Tirupathy'],
    'Akhyay Mohanty':[' Akhyay Mohanty',' Akshaya Mohanty'],
    'Ananya Sritam Nanda':[' Ananya Sritam Nanda',' Ananya Sriram Nanda',' Ananya Shritam Nanda'],
    'Anuradha Paudwal':[' Anuradha Paudwal',' Anuradha Poudwal'],
    'Papu Pom Pom': ['Papu Pom Pom'],
    'Subhasish Mahakud': ['Subhasish Mahakud','Subhashish'],
    'Jyotirmayee Nayak': ['Jyotirmayee Nayak',],
    'Mohammed Aziz': ['Mohammed Aziz','Md. Aziz'],
    'Kuldeep Pattanaik': ['Kuldeep Pattanaik', 'Kuldeep Pattnaik','Kuldeep Pattanaik Pattanaik','Kuldeep Pattanaik Pattanaik','Kuldeep Pattanaik Pattnaik'],
    'Humane Sagar': ['Humane Sagar'],
    'Nibedita': ['Nibedita'],
    'Mantu Chhuria': ['Mantu Chhuria','Mantu churia'],
    'Dipti Rekha Padhi': ['Dipti Rekha Padhi', 'Diptirekha Padhi','Diptirekha'],
    'Bijay Anand Sahu': ['Bijay Anand Sahu'],
    'Baidyanath Dash': ['Baidyanath Dash'],
    'Aseema Panda': ['Aseema Panda', 'Ashima Panda','Asima Panda','Asima','asima'],
    'Ipseeta Panda': ['Ipseeta Panda'],
    'Babool Supriyo': ['Babool Supriyo', 'Babul Supriyo'],
    'Arpita Choudhury': ['Arpita Choudhury', 'Arpita Chowdhury'],
    'Udit Narayan': ['Udit Narayan', 'Udit Naryan'],
    'Pamela Jain': ['Pamela Jain'],
    'Abinash Dash': ['Abinash Dash'],
    'Ananya Sritam Nanda': ['Ananya Sritam Nanda'],
    'Archana Padhi': ['Archana Padhi'],
    'Antara Chakraborty': ['Antara Chakraborty',' Antara Chakrabarty'],
    'Namita Agrawal': ['Namita Agrawal'],
    'Sonu Nigam': ['Sonu Nigam'],
    'Swayam Padhi': ['Swayam Padhi','swyam padhee', 'swyam padhi'],
    'Amrita Nayak ':['Amrita Nayak ','AMRITA NAYAK'],
    'Umakant Barik':['UMAKANT BARIK','Umakant Barik' ],
    'Unavailable':['E1']
    }

    for key, values in mapping.items():
        for value in values:
            audio_features['Artists'] = audio_features['Artists'].str.replace(value, key, case=False)

    return audio_features



def fetch_audio_features(Track_ids,df_songs,filtered_counts):
    
    """
    Fetches audio features for a list of track IDs and returns a DataFrame.

    Args:
        track_ids (list): List of track IDs.

    Returns:
        pandas.DataFrame: DataFrame containing audio features.

    """

    # key_rotator = SpotifyAPIKeyRotator(spotify_credentials)
    audio_features_data = []
    print_bold("Extracting Audio Features")
    for track_id in Track_ids:

        try:
            if track_id != 99999:
                audio_features = key_rotator.sp.audio_features(track_id)
                if audio_features:
                    features = audio_features[0]
                    audio_feature = {}

                    try:
                        audio_feature['Track ID'] = track_id
                    except:
                        audio_feature['Track ID'] = 99999

                    try:
                        audio_feature['Danceability'] = features.get('danceability')
                    except:
                        audio_feature['Danceability'] = 99999

                    try:
                        audio_feature['Energy'] = features.get('energy')
                    except:
                        audio_feature['Energy'] = 99999

                    try:
                        audio_feature['Acousticness'] = features.get('acousticness')
                    except:
                        audio_feature['Acousticness'] = 99999

                    try:
                        audio_feature['Duration (ms)'] = features.get('duration_ms')
                    except:
                        audio_feature['Duration (ms)'] = 99999

                    try:
                        audio_feature['Instrumentalness'] = features.get('instrumentalness')
                    except:
                        audio_feature['Instrumentalness'] = 99999

                    try:
                        audio_feature['Key'] = features.get('key')
                    except:
                        audio_feature['Key'] = 99999

                    try:
                        audio_feature['Liveness'] = features.get('liveness')
                    except:
                        audio_feature['Liveness'] = 99999

                    try:
                        audio_feature['Loudness'] = features.get('loudness')
                    except:
                        audio_feature['Loudness'] = 99999

                    try:
                        audio_feature['Mode'] = features.get('mode')
                    except:
                        audio_feature['Mode'] = 99999

                    try:
                        audio_feature['Speechiness'] = features.get('speechiness')
                    except:
                        audio_feature['Speechiness'] = 99999

                    try:
                        audio_feature['Tempo'] = features.get('tempo')
                    except:
                        audio_feature['Tempo'] = 99999

                    try:
                        audio_feature['Time Signature'] = features.get('time_signature')
                    except:
                        audio_feature['Time Signature'] = 99999

                    try:
                        audio_feature['Track Href'] = features.get('track_href')
                    except:
                        audio_feature['Track Href'] = 99999

                    try:
                        audio_feature['Valence'] = features.get('valence')
                    except:
                        audio_feature['Valence'] = 99999

                    audio_features_data.append(audio_feature)
                    
                
        
        except Exception as e:
            if e.http_status == 429 or e.http_status == 401:  # Rate limited or unauthorized
                print("Encountered rate limit or auth error, rotating credentials")
                key_rotator.rotate_credentials()

            else:
                # print(f"An error occurred for track ID {track_id}: {str(e)}")
                # print_bold(f"Error: {str(e)}\n")

                subject = 'Odia Spotify Scrapping Failed'
                output = f'Scraping Skipped some id"s: ' + str(e) + {track_id}
                
                sender_email = 'abc@gmail.com' #add sender email removed for safety purpose
                sender_password = 'abc'
                recipient_emails = ['abcd@gmail.com']


                sms.send_mail_alert(subject, output, sender_email, sender_password, recipient_emails)




            
    print("Audio Features extraction completed")
    audio_features = pd.DataFrame(audio_features_data)
    
    # Create a dictionary mapping TrackID to Artists from df1
    artist_dict = df_songs.set_index('TrackID')['Artists'].to_dict()
    # Add a new column 'Artists' to df2 using the TrackID column and the artist_dict
    audio_features['Artists'] = audio_features['Track ID'].map(artist_dict)
    
    # Create a dictionary mapping TrackID to Artists from df1
    Occurrences_dict = filtered_counts.set_index('TrackID')['Occurrences'].to_dict()
    # Add a new column 'Artists' to df2 using the TrackID column and the artist_dict
    audio_features['Occurrences'] = audio_features['Track ID'].map(Occurrences_dict)
    
    # Create a dictionary mapping TrackID to Artists from df1
    Release_Date_dict = df_songs.set_index('TrackID')['ReleaseDate'].to_dict()
    # Add a new column 'Artists' to df2 using the TrackID column and the artist_dict
    audio_features['Release_Date'] = audio_features['Track ID'].map(Release_Date_dict)

    audio_features = replace_artist_names(audio_features)
 
    return audio_features


def extract_playlist_details(playlist_df):
    """
    Extracts details of songs from a playlist and returns a list of filtered track IDs.

    Args:
        playlist_df (pandas.DataFrame): DataFrame containing playlist information.

    Returns:
        list: List of filtered track IDs.
    """


    # key_rotator = SpotifyAPIKeyRotator(spotify_credentials)
    df_songs = pd.DataFrame(columns=['PlaylistID', 'TrackID', 'TrackName', 'Artists', 'DurationMin', 'ISRC', 'Popularity',
                                     'ReleaseDate', 'AlbumID', 'AlbumName', 'AlbumType', 'TotalAlbumTracks', 'Timestamp'])

    filtered_track_ids = []
    

    

    Track_ID_Path =  r"C:\Users\nivet\Documents\Spotify Scraping\Track_Id_Data"
    
    Moutname_TrackID = "Track_Total_Ids_Data.xlsx"
    NewDataFileName_TrackID = "Track_New_id_data.xlsx"
    
    MfullPathname_TrackID = os.path.join(Track_ID_Path, Moutname_TrackID)
    NewDataFilePath_TrackID = os.path.join(Track_ID_Path, NewDataFileName_TrackID)

    
    
    Track_Details_Path_all =  r"C:\Users\nivet\Documents\Spotify Scraping\Track_Details_Data"
    
    Moutname_Track_all = "Track_Total_Details_Data.xlsx"
    NewDataFileName_Track_all = "Track_New_Details_data.xlsx"
    
    MfullPathname_Track_all = os.path.join(Track_Details_Path_all, Moutname_Track_all)
    NewDataFilePath_Track_all = os.path.join(Track_Details_Path_all, NewDataFileName_Track_all)
    

    try:
        print_bold("Extracting Playlist Details")
   
        for playlist_id in playlist_df['PlaylistID']:
            offset = 0
            total_tracks = 0

            while True:
                # Get playlist tracks with offset
                playlist_tracks = key_rotator.sp.playlist_tracks(playlist_id, offset=offset)

                # Retrieve the tracks
                tracks = playlist_tracks['items']

                for track in tracks:
                    try:
                        track_id = track['track']['id']
                    except:
                        track_id = 99999

                    try:
                        track_name = track['track']['name']
                        if track_name == '':
                            track_name =99999
                        else:
                            track_name = track_name
                    except:
                        track_name = 99999

                    try:
                        artists = [artist['name'] for artist in track['track']['artists']]
                        artists = ", ".join(artists)
                        
                        if artists == '':
                            artists =99999
                        else:
                            artists = artists
                    except:
                        artists =99999

                    try:
                        duration_ms = track['track']['duration_ms']
                        if duration_ms == 0:
                            duration_min = 99999
                        else:
                            duration_min = round(duration_ms / 60000, 2)
                    except:
                        duration_min = 99999

                    try:
                        isrc = track['track']['external_ids'].get('isrc', 'E1')
                    except:
                        isrc = 99999

                    try:
                        popularity = track['track']['popularity']
                    except:
                        popularity = 99999

                    try:
                        release_date = track['track']['album']['release_date']
                    except:
                        release_date = 99999

                    try:
                        album_id = track['track']['album']['id']
                    except:
                        album_id = 99999


                    try:
                        album_name = track['track']['album']['name']
                    except:
                        album_name = 99999

                    try:
                        album_type = track['track']['album']['album_type']
                    except:
                        album_type = 99999

                    try:
                        total_album_tracks = track['track']['album']['total_tracks']
                    except:
                        total_album_tracks = 99999

                  

                        
                    try:
                        Timestamp= Todays_TimeStamp
                    except:
                        Timestamp = 99999


                    song_data = [playlist_id, track_id, track_name, artists, duration_min, isrc, popularity,
                                 release_date, album_id, album_name, album_type, total_album_tracks,Timestamp]

                    df_songs.loc[len(df_songs)] = song_data

                # Increment the offset by the limit
                offset += len(tracks)
                total_tracks = playlist_tracks['total']

                # Break the loop if all tracks have been retrieved
                if offset >= total_tracks:
                    break

                # Sleep for a short duration to avoid rate limiting
                time.sleep(0.1)
                


        df_songs.dropna(subset=['TrackID', 'TrackName'], inplace=True)
        
  
        
        

        grouped_counts = df_songs.groupby(['TrackID', 'TrackName','Artists']).size().reset_index(name='Occurrences')

        sorted_counts = grouped_counts.sort_values(by='Occurrences', ascending=False)

        filtered_counts = sorted_counts[sorted_counts['Occurrences'] >= 2]

        filtered_track_ids = filtered_counts['TrackID'].tolist()

        filtered_counts['Timestamp'] = datetime.datetime.now()
        
    


        if len(filtered_counts) > 0:
            if os.path.exists(Track_ID_Path):
                if os.path.exists(MfullPathname_TrackID):
                    previous_Total_Track = pd.read_excel(MfullPathname_TrackID)
                    new_Track = filtered_counts[~filtered_counts['TrackID'].isin(previous_Total_Track['TrackID'])]
                    if os.path.exists(NewDataFilePath_TrackID):
                        previous_NewTrack = pd.read_excel(NewDataFilePath_TrackID)
                        filtered_counts_newTrack = pd.concat([previous_NewTrack, new_Track])
                        filtered_counts_newTrack.to_excel(NewDataFilePath_TrackID, index=False)
                    else:
                        new_Track.to_excel(NewDataFilePath_TrackID, index=False)
            else:
                os.makedirs(Track_ID_Path)
                filtered_counts.to_excel(NewDataFilePath_TrackID, index=False)
            
        if os.path.exists(MfullPathname_TrackID):
            previous_df_TrackId_data = pd.read_excel(MfullPathname_TrackID)
            new_TrackId = filtered_counts[~filtered_counts['TrackID'].isin(previous_df_TrackId_data['TrackID'])]
            filtered_counts_new = pd.concat([previous_df_TrackId_data, new_TrackId])
            filtered_counts_new.to_excel(MfullPathname_TrackID, index=False)
        else:
            filtered_counts.to_excel(MfullPathname_TrackID, index=False)



        print("Track Occurrence details extraction completed")

        if os.path.exists(Track_Details_Path_all):
            previous_df_Track_all = pd.read_excel(MfullPathname_Track_all)
            new_Track_all = df_songs[~df_songs['TrackID'].isin(previous_df_Track_all['TrackID'])]
            #df_songs_newTrack_all = pd.concat([previous_df_Track_all, new_Track_all])
            new_Track_all.to_excel(NewDataFilePath_Track_all, index=False)
        else:
            os.makedirs(Track_Details_Path_all)
            df_songs.to_excel(NewDataFilePath_Track_all, index=False)
            
        if os.path.exists(MfullPathname_Track_all):
            previous_df_TrackDetail_all = pd.read_excel(MfullPathname_Track_all)
            new_TrackDetails_all = df_songs[~df_songs['TrackID'].isin(previous_df_TrackDetail_all['TrackID'])]
            df_songs_new_all = pd.concat([previous_df_TrackDetail_all, new_TrackDetails_all])
            df_songs_new_all.to_excel(MfullPathname_Track_all, index=False)
        else:
            df_songs.to_excel(MfullPathname_Track_all, index=False)
   
        print('Playlist Track Details extraction completed')



        
    except Exception as e:
        if e.http_status == 429 or e.http_status == 401:  # Rate limited or unauthorized
            print("Encountered rate limit or auth error, rotating credentials")
            key_rotator.rotate_credentials()



        else:
            traceback_str = traceback.format_exc()
            print(f"An error occurred while extracting playlist details:\n{str(e)}")
            print(f"Traceback:\n{traceback_str}")
        
        
 

    return filtered_track_ids, df_songs, filtered_counts

def get_playlist_id(queries):

    """
    Retrieves playlists containing Odia language-related terms.

    Args:
        queries (list): List of search queries.

    Returns:
        pandas.DataFrame: DataFrame containing playlist information.

    Raises:
        ValueError: If queries is not a list.

    """
    # key_rotator = SpotifyAPIKeyRotator(spotify_credentials)
    # print('in:   ', key_rotator)

    PlayList_Id_Path =  r"C:\Users\nivet\Documents\Spotify Scraping\Playlist_Id_Data"
    
    Moutname = "PlayList_Total_Ids_Data.xlsx"
    NewDataFileName = "PlayList_New_id_data.xlsx"
    
    MfullPathname_playlist = os.path.join(PlayList_Id_Path, Moutname)
    NewDataFilePath_playlist = os.path.join(PlayList_Id_Path, NewDataFileName)

    if not isinstance(queries, list):
        raise ValueError("Queries must be a list.")

    odia_terms = ['odia', 'oriya', ' ollywood', 'odisha']
    additional_terms = ['english', 'hindi', 'tamil','gujarati','bengali', 'bangla', 'marati', 'punjabi', 'kerala', 'mollywood', ' malayalam', 'mallu']
    playlist_info = []

    try:
        print('\n\n')
        print('Date Scrapped:',Todays_TimeStamp)
        print_bold("Retrieving Playlists")
        print("Processing search query")
        for index, search_query in enumerate(queries):
            search_results = key_rotator.sp.search(q=search_query, type='playlist', market='IN', limit=3)

            for playlist in search_results['playlists']['items']:
                playlist_id = playlist['id']
                playlist_name = playlist['name']
                num_songs = playlist['tracks']['total']

                pattern = r'\b(?:' + '|'.join(odia_terms) + r')\b'
                # if re.search(pattern, playlist_name, flags=re.IGNORECASE):
                if re.search(pattern, playlist_name, flags=re.IGNORECASE) and not any(term in playlist_name.lower() for term in additional_terms):
                    playlist_info.append({
                        'PlaylistID': playlist_id,
                        'PlaylistName': playlist_name,
                        'NumSongs': num_songs,
                        'Timestamp': Todays_TimeStamp
                    })

        playlist_df = pd.DataFrame(playlist_info)
        playlist_df = playlist_df.drop_duplicates(subset='PlaylistID')
        print("Playlist retrieval completed")
    
        playlist_new_df = playlist_df.copy()

        if os.path.exists(PlayList_Id_Path):
            previous_df = pd.read_excel(MfullPathname_playlist)
            new_playlists = playlist_new_df[~playlist_new_df['PlaylistID'].isin(previous_df['PlaylistID'])]
            new_playlists.to_excel(NewDataFilePath_playlist, index=False)
        else:
            os.makedirs(PlayList_Id_Path)
            playlist_df.to_excel(NewDataFilePath_playlist, index=False)

        if os.path.exists(MfullPathname_playlist):
            previous_df_playlist = pd.read_excel(MfullPathname_playlist)
            new_playlist_df = playlist_df[~playlist_df['PlaylistID'].isin(previous_df_playlist['PlaylistID'])]
            new_updated_playlist_df = pd.concat([previous_df_playlist, new_playlist_df])
            new_updated_playlist_df.to_excel(MfullPathname_playlist, index=False)
        else:
            playlist_df.to_excel(MfullPathname_playlist, index=False)


        return playlist_df
  
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429 or e.http_status == 401:  # Rate limited or unauthorized
            print("Encountered rate limit or auth error, rotating credentials")
            key_rotator.rotate_credentials()


        else:
            print(f"Error: {str(e)}")
            traceback.print_exc()
            return pd.DataFrame()
        

# Redirect stderr to a file to suppress warnings
#sys.stderr = open("error_log.txt", "w")

import datetime
Todays_TimeStamp = datetime.datetime.now()

key_rotator = SpotifyAPIKeyRotator(spotify_credentials)
print('out:   ', key_rotator)
   
def get_main(queries):
    """
    Fetches audio features for a given list of queries.

    Args:
        queries (list): List of queries to search for playlists.

    Returns:
        list: A list of audio features for the tracks in the playlists.

    Raises:
        ValueError: If queries is not a list.

    """

    if not isinstance(queries, list):
        raise ValueError("Queries must be a list.")
    
    try:

 
        playlist_df = get_playlist_id(queries)
        # print(Todays_TimeStamp, 'Spotify Scrapping Started ')

        print_bold("Successfully Retrieved playlist IDs")

        Track_ids,df_songs,filtered_counts = extract_playlist_details(playlist_df)
        print_bold("Successfully Retrieved track IDs" )

        audio_features = fetch_audio_features(Track_ids,df_songs,filtered_counts)
        print_bold("Successfully Retrieved audio features")

        Clustered_Audio_Features = cluster_features(audio_features)
        print_bold("Successfully Retrieved Clustered_Audio_Features")

        subject = 'Odia Spotify Scrapping Successful'
        output = 'Scraping Success'



    except Exception as e:

        print_bold(f"Error: {str(e)}\n")

        subject = 'Odia Spotify Scrapping Failed'
        output = 'Scraping Failed: ' + str(e)
        
        sender_email = 'abc@gmail.com' #add sender email removed for safety purpose
        sender_password = 'abc'
        recipient_emails = ['abcd@gmail.com']
  
    # Send email notification
        sms.send_mail_alert(subject, output, sender_email, sender_password, recipient_emails)
        return []
    
        sender_email = 'abc@gmail.com' #add sender email removed for safety purpose
        sender_password = 'abc'
        recipient_emails = ['abcd@gmail.com']

    # Send email notification
    sms.send_mail_alert(subject, output, sender_email, sender_password, recipient_emails)
    
    
# to run in locally remove the comments 
# df_Queries = pd.read_excel("Queries_CG.xlsx")
# queries = df_Queries['Queries'].to_list()
                           
# get_main(queries)
