import pandas as pd
import streamlit as st
import plotly.express as px

# Assuming df1, df2, df3, df4, df5, and df6 are your DataFrames

# file_path =r"/home/muzik247/mnt/BACKUP_RUN_BY_MANUAL/Spotify_Scrapping/Spotify Report Data.xlsx"
file_path =r"/home/muzik247/mnt/DEPLOYED_WEB_APPS/Spotify_Report_Data_monitor/Odia/Spotify Report Data Odia.xlsx"



def replace_publisher_names(df):
    mapping = {
    'Sidharth Music': ['sarthak music (p) ltd','sarthak music pvt. ltd.','Sarthak Music Pvt Ltd','Sarthak Music (P) Ltd',
                      'Sarthak Music Pvt. Ltd.'],
        
    'Funny Angulia':['Funny Angulia Official','Funny Anugulia']
    }

    for key, values in mapping.items():
        for value in values:

            df['Publisher Name'] = df['Publisher Name'].str.replace(value, key, case=False)

    return df



df1 = pd.read_excel(file_path, sheet_name='top_song_details')
df1['Publisher Name'] = df1['Publisher Name'].str.replace('â„—  ','').str.replace('(C)  ','')
df1['Publisher Name'] = df1['Publisher Name'].str.strip()
df1 = replace_publisher_names(df1)

df2 = pd.read_excel(file_path, sheet_name='Music Label Occurence')
df2.fillna(0,inplace=True)


df3 = pd.read_excel(file_path, sheet_name='Artist Growth from 2019')
df3.fillna(0, inplace=True)
df3.drop(['Remarks'], axis=1, inplace=True)



df4 = pd.read_excel(file_path, sheet_name='artist_top')
df4.fillna(0,inplace=True)

df5 = pd.read_excel(file_path, sheet_name='Unique Artists Growth')
df5.fillna(0,inplace=True)

df6 = pd.read_excel(file_path, sheet_name='individual year artist growth')
df6.fillna(0,inplace=True)





# Streamlit app
st.title("Spotify Data Report")

# Sidebar for selecting the dataset
selected_dataset = st.sidebar.radio('Select Dataset', ['Top Labels', 'Music Label Growth', 'Artist Growth from 2019', 'Top Artists', 'Unique Artists', 'Individual Artist Growth'])

if selected_dataset == 'Top Labels':
    df = df1
    # Add the code for value_counts_df1 here
    value_counts_df1 = df1['Publisher Name'].value_counts()
    # st.title("Top Songs Music Labels of Playlist")
    st.markdown("<h2 style='font-size:24px;'>Top Songs Music Labels of Playlist</h2>", unsafe_allow_html=True)
    # Sidebar for selecting the threshold
    selected_threshold = st.sidebar.selectbox(
        'Select Threshold',
        [1, 2, 3, 5],  # Add or modify thresholds as needed
        index=3  # Set the default threshold index
    )

    # Filter values based on the selected threshold
    filtered_counts = value_counts_df1[value_counts_df1 >= selected_threshold]

    # Sort values in descending order
    filtered_counts = filtered_counts.sort_values(ascending=False)

    # Create a bar graph using Plotly
   # Create a bar graph using Plotly
    fig = px.bar(
        x=filtered_counts.index,  # Change x to Publisher Name
        y=filtered_counts.values,  # Change y to Count
        labels={'x': 'Publisher Name', 'y': 'Count'},  # Swap labels
        title=f'Music Label Occurrence (Count >= {selected_threshold})',
        orientation='v'  # Keep orientation vertical
    )

    # Annotate each bar with its count without arrow
    for i, count in enumerate(filtered_counts.values):
        fig.add_annotation(
            x=filtered_counts.index[i],  # Change x to Publisher Name
            y=count,  # Change y to Count
            text=str(count),
            yshift=10,
            showarrow=False  # Remove arrow
        )

    # Adjust figure size
    fig.update_layout(
        height=600,  # Set the height of the graph
        width=1000,  # Set the width of the graph
    )

    # Display the plot
    st.plotly_chart(fig)


elif (selected_dataset == 'Music Label Growth') or (selected_dataset == 'Artist Growth from 2019') or ( selected_dataset == 'Top Artists') :

    if selected_dataset == 'Music Label Growth':
        df = df2

        # df['Publisher'] = df['Publisher'].str.replace('â„—  ','').str.replace('(C)  ','')
        # df['Publisher'] = df['Publisher'].str.strip()
        # df = replace_publisher_names(df1)








        show_all_option = True
        # st.title("Music Labels Growth")
        st.markdown("<h2 style='font-size:24px;'>Music Labels Growth</h2>", unsafe_allow_html=True)
    elif selected_dataset == 'Artist Growth from 2019':
        df = df3
        show_all_option = True
        st.markdown("<h2 style='font-size:24px;'>Artist Growth from 2019</h2>", unsafe_allow_html=True)
        # st.title("Artist Growth from 2019")

    elif  selected_dataset == 'Top Artists':
         df = df4
         show_all_option = True
         st.markdown("<h2 style='font-size:24px;'>Top Songs Artists Playlist</h2>", unsafe_allow_html=True)



    # Dropdown for selecting the month
    selected_month_options = ['All'] + list(df.columns[1:]) if show_all_option else list(df.columns[1:])
    selected_month = st.selectbox(
        'Select Month',
        selected_month_options
    )




    # Filter DataFrame based on the selected month
    if selected_month == 'All':
        if 'Publisher' in df.columns:
            df_melted = pd.melt(df, id_vars='Publisher', var_name='Month', value_name='Count')
        else:
            df_melted = pd.melt(df, id_vars='Artist_Name', var_name='Month', value_name='Count')
    else:
        df_monthly = df[['Publisher', selected_month]] if 'Publisher' in df.columns else df[['Artist_Name', selected_month]]
        df_melted = pd.melt(df_monthly, id_vars='Publisher' if 'Publisher' in df.columns else 'Artist_Name', var_name='Month', value_name='Count')

    # Create the grouped bar plot with unique colors for each publisher or artist
    fig = px.bar(
        df_melted,
        x='Month',
        y='Count',
        color='Publisher' if 'Publisher' in df.columns else 'Artist_Name',
        title=f'Monthly Data for Publishers - {selected_month}',
        labels={'Count': 'Value'},
        height=600,
        width=1000,
        barmode='group',
        color_discrete_map={pub: f'#{hash(pub) & 0xffffff:06x}' for pub in df_melted['Publisher'].unique()} if 'Publisher' in df.columns
        else {artist: f'#{hash(artist) & 0xffffff:06x}' for artist in df_melted['Artist_Name'].unique()}
    )

    # Display the plot
    st.plotly_chart(fig)







else:
    show_all_option = False
    
    if selected_dataset == 'Unique Artists' :
        df = df5
        year_column = 'Song_Released_Year'
        # st.title("Unique Artists")
        st.markdown("<h2 style='font-size:24px;'>Unique Artists</h2>", unsafe_allow_html=True)
       
    elif selected_dataset == 'Individual Artist Growth':
        df = df6
        year_column = 'Year'
        # st.title("Individual Artist Growth")
        st.markdown("<h2 style='font-size:24px;'>Individual Artist Growth</h2>", unsafe_allow_html=True)
      

 

    # Sidebar for selecting the year
    selected_year = st.sidebar.selectbox('Select Year', df[year_column].unique())

    # Filter DataFrame based on the selected year
    df_selected = df[df[year_column] == selected_year]

    # df_selected = df_selected[['Artist_Name', 'June 2023', 'July 2023', 'August 2023', 'September 2023',
    #                         'October 2023', 'November 2023', 'December 2023']]

    columns_to_select = [col for col in df.columns if col != year_column]

    
    df_selected1 = df_selected[columns_to_select]


    df_melted = pd.melt(df_selected1, id_vars='Artist_Name', var_name='Month', value_name='Count')

    # Create the grouped bar plot with unique colors for each artist
    fig = px.bar(df_melted, x='Month', y='Count', color='Artist_Name',
                title=f'Monthly Growth for Artist song Released in {selected_year}',
                labels={'Count': 'Value'},
                height=600,
                width=1000,
                barmode='group',  # Set barmode to 'group' for grouped bars
                color_discrete_map={artist: f'#{hash(artist) & 0xffffff:06x}' for artist in
                                    df_melted['Artist_Name'].unique()})

    # Display the plot
    st.plotly_chart(fig)