from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from psycopg2 import OperationalError  # For error handling with PostgreSQL
import config
import streamlit as st

@st.cache_resource(ttl="1h")  # Cache for 1 hour
def create_database_connection():
    """
    Establish a connection to the PostgreSQL database using SQLAlchemy and LangChain's SQLDatabase utility.

    Returns:
        SQLDatabase: A connection to the database if successful; otherwise, raises an OperationalError.
    """
    try:
        # Use DATABASE_URL from config, which gets it from Streamlit secrets
        db = SQLDatabase(create_engine(config.DATABASE_URL))
        return db
    except OperationalError:
        raise OperationalError("Database connection failed. Please check your credentials or network connection.")
