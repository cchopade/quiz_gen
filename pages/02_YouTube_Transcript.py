# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 07:44:24 2024

@author: Chinmay.Chopade
"""

from pytube import YouTube
import streamlit as st
import openai
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

            #try:
                video = YouTube(video_url)
                st.success("Video fetched")
                duration = video.length
                # filtering the audio. File extension can be mp4/webm
                audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
                st.success("Audio stream filtered")
                audio.download(filename="audio.mp4")
                st.success('Download Completed!')
                         
            #except:
                #st.write("Connection Error")  # to handle exception
                
            audio_file = open("audio.mp4", "rb")
            transcription_cost = round(round(duration/60,2)*0.006,4)
            st.write(f'Estimated trasncription cost = USD {transcription_cost}')
            
            transcript = openai.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_file
                                )
            st.write(transcript.text)
            