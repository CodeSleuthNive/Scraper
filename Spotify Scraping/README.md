# Overview


This code automates the extraction, processing, and clustering of Odia music-related playlists and tracks from Spotify, using multiple rotating API keys to manage rate limits. It also sends email notifications for both successful runs and any errors encountered.


# Key Features

### API Key Rotation:
  Automatically rotates through multiple Spotify API keys to handle rate limiting and authentication errors.
  
### Data Extraction: 
  Fetches playlist details and audio features for tracks based on Odia language-related queries.
  
### Feature Clustering: 
  Groups audio features into clusters, allowing for analysis of track characteristics.
  
### Automated Alerts: 
  Sends email notifications to specified recipients upon successful execution or if errors occur.

  
#  Functions
###  SpotifyAPIKeyRotator: 
  Manages and rotates Spotify API keys for stable data extraction.
###  get_playlist_id: 
  Retrieves playlists related to Odia music based on search queries.
###  extract_playlist_details: 
  Extracts track details from playlists, filtering for duplicates.
### fetch_audio_features: 
  Gathers audio features of each track, handling API responses and errors.
###  cluster_features: 
  Performs clustering on extracted audio features and saves results.

