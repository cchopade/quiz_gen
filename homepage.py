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
st.title("AI Tools")

st.write("Click on the items on the left sidebar to access all he tools")

