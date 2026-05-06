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

if st.button("Stwórz pomysły na kolorowanki"):
    szczegoly = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=list[ColoringPage],
        messages=[
            {
                "role": "system",
                "content": "Jesteś ekspertem w tworzeniu opisów wizualnych dla czarno-białych kolorowanek liniowych. "
                           "Każdy wygenerowany pomysł MUSI mieć unikalny, kreatywny i opisowy tytuł odnoszący się do konkretnej akcji (np. 'Spotkanie z Ośmiornicą Strażnikiem Skarbu' zamiast nudnego 'Kolorowanka 1'). "
                           "Kiedy tworzysz `visual_description`, opisuj tylko kształty i linie. **NIGDY** nie używaj nazw kolorów (np. 'zielony', 'czerwony'). Używaj słów, które opisują fakturę lub jasność, ale tylko w czarno-białym kontekście."
            },
            {
            "role": "user", 
            "content": f"Stwórz szczegółowe opisy dla kolorowanek w liczbie {liczba_pomyslow}. Temat od użytkownika: {temat_kolorowanki}."
            }
            ]

    )
    st.session_state.pomysly = szczegoly
    #st.write(szczegoly)

if "pomysly" in st.session_state:

    st.divider()

    wybrane_pomysly = st.multiselect(
        "Wybierz pomysł, który najbardziej Ci się podoba:",
        options=st.session_state.pomysly,
        format_func=lambda opcja: opcja.title
    )

    ilosc_rysunkow = st.slider(
        "Ile wariantów kolorowanki wygenerować dla KAŻDEGO wybranego pomysłu?", 
        min_value=1, max_value=3, value=1
    )
    
    st.write(f"Wybrano pomysłów: {len(wybrane_pomysly)}")
    st.write(f"Do wygenerowania łącznie: {len(wybrane_pomysly) * ilosc_rysunkow} obrazków.")

   