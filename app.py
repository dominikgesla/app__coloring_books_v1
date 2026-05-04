import streamlit as st
import instructor
import openai
from pydantic import BaseModel 
from dotenv import load_dotenv

load_dotenv()

class ColoringPage(BaseModel):
    title: str
    difficulty: int
    number_of_elements: int
    recipient_age: int
    visual_description: str

st.title("Generator kolorowanek")