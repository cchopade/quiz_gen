# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 17:31:51 2024

@author: Chinmay.Chopade
"""

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
st.title("MCQ Quiz Generator")

# Input text from user
text = st.text_area("Input the text:", height=300)

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
    if not text:
        st.error("Please input the text to generate questions.")
    else:
        with st.spinner("Generating questions..."):
            response = generate_mcq_questions(text, num_questions, difficulty, num_options)
            st.success("Questions generated successfully!")

            # Parse the response and return
            questions = response.choices[0].message.content
            
            #calculate the tokens and the estimaed cost
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = round(input_tokens*(5/1000000)+output_tokens*(15/1000000),4)
            st.write(f'Total estimaed cost = USD {cost}')
            
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
            
            