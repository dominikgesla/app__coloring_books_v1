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

if "generation_id" not in st.session_state:
    st.session_state.generation_id = 0   

if st.button("Stwórz pomysły na kolorowanki"):
    if not temat_kolorowanki.strip():
        st.warning("⚠️ Hej! Zanim wygenerujesz pomysły, wpisz najpierw temat w polu powyżej.")
    else:
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
        st.session_state.generation_id += 1


if "pomysly" in st.session_state:

    st.divider()
    st.subheader("🧐 Przejrzyj propozycje")

    # Sekcja podglądu dla każdego pomysłu. Zastosowany enumerate, aby uzyskać unikalny indeks (idx) dla każdego pomysłu
    for idx, p in enumerate(st.session_state.pomysly):
        with st.expander(f"🖼️ {p.title}"):
            # Trzy kolumny na parametry
            c1, c2, c3 = st.columns(3)
            bezpieczna_liczba = max(1, min(p.number_of_elements, 150))
            # edytowalne pola metryk, wartością domyślną jest propozycja wygenerowana przez AI
            p.recipient_age = c1.number_input("Wiek dziecka", min_value=2, max_value=16, value=p.recipient_age, key=f"wiek_{idx}_{st.session_state.generation_id}")
            p.number_of_elements = c2.number_input("Liczba elementów", min_value=1, max_value=150, value=bezpieczna_liczba, key=f"elem_{idx}_{st.session_state.generation_id}")
            p.difficulty = c3.slider("Trudność (1-5)", min_value=1, max_value=5, value=p.difficulty, key=f"trud_{idx}_{st.session_state.generation_id}")
            
            # Duże, w pełni edytowalne pole tekstowe
            p.visual_description = st.text_area(
                "Opis dla generatora kolorowanek (możesz dowolnie modyfikować):", 
                value=p.visual_description, 
                height=150, # Wysokość pola w pikselach
                key=f"opis_{idx}_{st.session_state.generation_id}"
            )

    st.divider()

    wybrane_pomysly = st.multiselect(
        "Zaznacz, które z powyższych pomysłów chcesz narysować:",
        options=st.session_state.pomysly,
        format_func=lambda opcja: opcja.title
    )

    ilosc_rysunkow = st.slider(
        "Ile wariantów kolorowanki wygenerować dla KAŻDEGO wybranego pomysłu?", 
        min_value=1, max_value=3, value=1
    )
    
    st.write(f"Wybrano pomysłów: {len(wybrane_pomysly)}")
    st.write(f"Do wygenerowania łącznie: {len(wybrane_pomysly) * ilosc_rysunkow} obrazków.")

   