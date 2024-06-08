# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 08:15:22 2024

@author: Chinmay.Chopade
"""

import streamlit as st
import openai
import pandas as pd
import json
import os
from dotenv import load_dotenv
from pytube import YouTube

try:
    load_dotenv()
    openai.api_key=os.getenv("OPENAI_API_KEY")
    PASSPHRASE = os.getenv("PASSPHRASE")
except:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    PASSPHRASE = st.secrets["PASSPHRASE"]


# Set the title of the Streamlit app
st.title("YouTube to Quiz Generator")

# Input text from user
video_url = st.text_input("Input the YouTube video link:")

# Number of questions
num_questions = st.number_input("Number of questions (max 50):", min_value=1, max_value=50, step=1)

# Difficulty level
difficulty = st.selectbox("Select difficulty level:", ["easy", "medium", "hard"])

# Number of options per question
num_options = st.number_input("Number of options per question (2 to 6):", min_value=2, max_value=6, step=1)

#passphrase box
user_passphrase = st.text_input("Enter a passphrase", type="password")

# Generate questions button
generate_btn = st.button("Generate Questions")

json_f = json.loads(
    """
        [
            {
              "question": "What is the fundamental object in string theory that replaces point-like particles?",
              "options": ["Waves","Strings","Quarks","Bosons"],
              "answer": "Strings",
              "explaination": "Strings replaces the point-like particles in string theory"
            },

            {
              "question": "What is the fundamental object in string theory that replaces point-like particles?",
              "options": ["Waves","Strings","Quarks","Bosons"],
              "answer": "Strings",
              "explaination": "Strings replaces the point-like particles in string theory"
            }            

        ]
    
    """)

def generate_mcq_questions(text, num_questions, difficulty, num_options):

    # Prompt for OpenAI
    prompt = f"Generate {num_questions} multiple-choice questions based on the following text. Each question should have {num_options} options and the difficulty level should be {difficulty}.Provide correct answer and the explaination for the correct answer. Text: {text}. Generate response in JSON format.Following the sample JSON {json_f}"       
            
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":prompt}
            ],
        #max_tokens=1500,  # Adjust based on response size
        n=1,
        stop=None,
        temperature=0.7,
        response_format={ "type": "json_object" }
    )
    return response

if generate_btn and user_passphrase == PASSPHRASE:
    if not video_url:
        st.error("Please input the text to generate questions.")
    else:
        with st.spinner("Trasncribing..."):
            try:
                video = YouTube(video_url)
                # filtering the audio. File extension can be mp4/webm
                # You can see all the available streams by print(video.streams)
                audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
                #audio.download(filename="audio.mp4")
                st.write('Download Completed!')
            
            except:
                st.write("Connection Error")  # to handle exception
                
                
            audio_file = open(audio, "rb")
            
            transcript = openai.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_file
                                )
            text = transcript.text
            st.write('Transcription Completed!')
            
        with st.spinner("Generating questions..."):
            response = generate_mcq_questions(text, num_questions, difficulty, num_options)
            st.success("Questions generated successfully!")

            # Parse the response and return
            questions = response.choices[0].message.content
            
            
            #write the questions to the screen
            st.json(questions)
            
            # convert to csv and provide option to download questions as CSV
            csv_questions = json.loads(questions)['questions']
            csv = pd.DataFrame.from_records(csv_questions).to_csv(index=False).encode('utf-8')
            
            #csv = pd.read_json(questions).to_csv(index=False).encode('utf-8')
            st.download_button(label="Download questions as CSV",
                               data=csv,
                               file_name='mcq_questions.csv',
                               mime='text/csv')
            
            