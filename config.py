import streamlit as st

# Fetching secrets from Streamlit's secrets manager
DATABASE_URL = st.secrets["DATABASE_URL"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
