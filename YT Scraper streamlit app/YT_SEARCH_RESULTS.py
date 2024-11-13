from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import streamlit as st
import base64



st.header("Youtube Search Results Videos Scrapper")


with st.form("My_form"):
    title = st.text_input('Enter the search term')
    s_nos = st.text_input('Enter Number of Scrolls Default Val is 25', value='25')
    s_nos=int(s_nos)
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("PROCESSING PLEASE WAIT")
        if len(title)==0:
            st.write("Enter Something")
            st.stop()
        my_bar = st.progress(0, text="STARTED")
        options=webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        prefs = {"profile.managed_default_content_settings.images":2}
        options.add_experimental_option("prefs",prefs)





        driver = webdriver.Chrome(options=options)
        driver.get("https://www.youtube.com")

        search_box = driver.find_element_by_name('search_query')
        search_box.send_keys(title)
        search_box.submit()

        SCROLL_PAUSE_TIME = 1.5

        # Scroll down to load more content
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        ct=0
        while ct<s_nos:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            ct+=1
            #my_bar.progress(ct*4, text="LOADING")
        # Wait for search results to load
        time.sleep(10)

        video_elements = driver.find_elements_by_css_selector('ytd-video-renderer')

        #print("#########################################", len(video_elements))

        video_details = []
        ct=0
        for video_element in video_elements:
                #print(ct)
                sentance = video_element.text.split("\n")
                if len(sentance[0]) < 9:
                    sentance = sentance[1:]

                vid_link=video_element.find_element_by_id("video-title").get_attribute('href')
                ch_link=video_element.find_element_by_id("channel-thumbnail").get_attribute('href')
                #print("len",len(sentance))
                if len(sentance)==5:
                    #print("sent", sentance)
                    video_details.append({
                        'Title': sentance[0],
                        'Views':sentance[1],
                        'Published':sentance[2],

                        'Channel': sentance[3],
                        'Description':sentance[4],
                        'Channle_link':ch_link,
                        'Video_link':vid_link
                    })
                else:
                    #print("len",len(sentance))
                    video_details.append({
                        'Title': sentance[0],
                        'Views':sentance[1],
                        'Published':sentance[2],

                        'Channel': -1,
                        'Description':-1,
                        'Channle_link':ch_link,
                        'Video_link':vid_link
                    })
                ct+=1

        dft = pd.DataFrame(video_details)
        def get_vid(x):
            try:
                vid=x.split('=')[1][:11]
                return vid
            except:
                return x[-11:]

        def classify(x):
            try:
                vid=x.split('=')[1][:11]
                return "VIDEO"
            except:
                return "SHORTS"

        dft["Video_id"]=dft['Video_link'].apply(get_vid)
        dft["Vid_Type"]=dft['Video_link'].apply(classify)
        dft["Search_Query"]=title    
        print(dft.shape)
        #st.subheader("Please wait for complete load, ignore for warning and errors")
        # Display the header
        st.header("RESULTS")

        # Display the total number of results
        st.subheader(f"TOTAL NO OF RESULTS: {len(dft)}")

        # Display the total number of videos
        total_videos = len(dft[dft["Vid_Type"] == "VIDEO"])
        st.subheader(f"TOTAL NO OF Videos: {total_videos}")

        # Display the total number of shorts
        total_shorts = len(dft[dft["Vid_Type"] == "SHORTS"])
        st.subheader(f"TOTAL NO OF Shorts: {total_shorts}")
        st.subheader("Data Frame")
        st.dataframe(dft)

        def download_csv():
            csv = dft.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Encode the DataFrame to base64
            href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
            return href

        st.markdown(download_csv(), unsafe_allow_html=True)

        driver.quit()