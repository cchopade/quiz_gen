# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 07:44:24 2024

@author: Chinmay.Chopade
"""

from pytube import YouTube
import streamlit as st
import openai
import pandas as pd
import json
import os
from dotenv import load_dotenv

try:
    load_dotenv()
    openai.api_key=os.getenv("OPENAI_API_KEY")
    PASSPHRASE = os.getenv("PASSPHRASE")
except:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    PASSPHRASE = st.secrets["PASSPHRASE"]


# Set the title of the Streamlit app
st.title("YouTube Transcript Generator")

# Input text from user
video_url = st.text_input("Input the YouTube video link:")

# Generate questions button
generate_btn = st.button("Generate Transcript")

if generate_btn:
    if not video_url:
        st.error("Please input the URL to generate questions.")
    else:
        with st.spinner("Generating transcript..."):

            try:
                video = YouTube(video_url)
                st.write("video loaded")
                # filtering the audio. File extension can be mp4/webm
                # You can see all the available streams by print(video.streams)
                audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
                st.write("audio stream filtered")
                audio.download(filename="audio.mp4")
                st.write('Download Completed!')
                
            except:
                st.write("Connection Error")  # to handle exception
                
            audio_file = open("audio.mp4", "rb")
            
            transcript = openai.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_file
                                )
            st.write(transcript.text)