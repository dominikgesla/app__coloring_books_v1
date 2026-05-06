import streamlit as st
import instructor
import openai
from pydantic import BaseModel 
from dotenv import load_dotenv

load_dotenv()

client = instructor.from_openai(openai.OpenAI())

class ColoringPage(BaseModel):
    title: str
    difficulty: int
    number_of_elements: int
    recipient_age: int
    visual_description: str

st.title("Generator kolorowanek")
temat_kolorowanki = st.text_input ("Opisz, co ma byc na kolorowance")
liczba_pomyslow = st.slider("Ile pomysłów chcesz wygenerować?", min_value=1, max_value=5, value=3)
if st.button("Stwórz kolorowankę"):
    szczegoly = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=list[ColoringPage],
        messages=[
            {
                "role": "system",
                "content": "Jesteś ekspertem w tworzeniu opisów wizualnych dla czarno-białych kolorowanek liniowych. Kiedy tworzysz `visual_description`, opisuj tylko kształty i linie. **NIGDY** nie używaj nazw kolorów (np. 'zielony', 'czerwony'). Używaj słów, które opisują fakturę lub jasność, ale tylko w czarno-białym kontekście."
            },
            {
            "role": "user", 
            "content": f"Stwórz szczegółowe opisy dla kolorowanek w liczbie {liczba_pomyslow}. Temat od użytkownika: {temat_kolorowanki}."
            }
            ]

    )
    st.write(szczegoly)
   

   