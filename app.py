import streamlit as st
import instructor
import openai
import os
from pydantic import BaseModel 
from dotenv import load_dotenv
import json
import requests
print(f"DEBUG: Klucz w systemie: {os.environ.get('OPENAI_API_KEY')}")

load_dotenv()

# ==========================================
# WERYFIKACJA KLUCZA API
# ==========================================
st.sidebar.header("🔑 Ustawienia API")

# Próbujemy pobrać klucz z ukrytego środowiska (np. pliku .env)
api_key = os.environ.get("OPENAI_API_KEY")

# Jeśli klucza nie znaleziono 
if not api_key:
    api_key = st.sidebar.text_input("Wklej swój klucz OpenAI API:", type="password")
    
    if not api_key:
        # Jeśli użytkownik jeszcze nic nie wpisał, pokazujemy komunikat i ZATRZYMUJEMY aplikację
        st.info("💡 Aplikacja wymaga klucza OpenAI do działania. Wprowadź go w panelu bocznym po lewej stronie.")
        st.stop() # 🛑 Szlaban! Streamlit nie czyta kodu poniżej tej linijki.

# Jeśli kod dotarł tutaj, to znaczy, że mamy klucz (z pliku lub od użytkownika)
# Inicjalizujemy aplikacje z użyciem tego konkretnego klucza
client = instructor.from_openai(openai.OpenAI(api_key=api_key))

class ColoringPage(BaseModel):
    title: str
    difficulty: int
    number_of_elements: int
    recipient_age: int
    visual_description: str

st.sidebar.header("📁 Zarządzanie sesją")

plik_sesji = st.sidebar.file_uploader("Wczytaj zapisaną sesję (plik JSON)", type=["json"])

if plik_sesji is not None:
    try:
        # Odczytuje dane z pliku
        dane_z_pliku = json.load(plik_sesji)
        # Zmieniam zwykły tekst z powrotem na nasze specjalne obiekty ColoringPage
        # Używam operatora ** (rozpakowanie słownika), aby odtworzyć obiekty
        st.session_state.pomysly = [ColoringPage(**element) for element in dane_z_pliku]
        
        # Zabezpieczenie dla generowania nowych kluczy widgetów
        if "generation_id" not in st.session_state:
            st.session_state.generation_id = 999 
            
        st.sidebar.success("✅ Sesja wczytana pomyślnie!")
    except Exception as e:
        st.sidebar.error("❌ Błąd wczytywania pliku. Upewnij się, że to poprawny plik sesji.")

st.title("Generator kolorowanek")

temat_kolorowanki = st.text_input ("Opisz, co ma byc na kolorowance")

liczba_pomyslow = st.slider("Ile pomysłów chcesz wygenerować?", min_value=1, max_value=5, value=3)

if "generation_id" not in st.session_state:
    st.session_state.generation_id = 0   

if "wygenerowane_obrazki" not in st.session_state:
    st.session_state.wygenerowane_obrazki = []

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

    st.sidebar.divider()
    st.sidebar.subheader("Zapisz obecne pomysły")
    
    dane_do_zapisu = [p.model_dump() for p in st.session_state.pomysly]
    sesja_json = json.dumps(dane_do_zapisu, ensure_ascii=False, indent=4)
    
    st.sidebar.download_button(
        label="💾 Pobierz sesję na dysk",
        data=sesja_json,
        file_name="moje_pomysly_na_kolorowanki.json",
        mime="application/json"
    )

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

    st.divider()
    
    if st.button("Wygeneruj wybrane rysunki"):
        
        if not wybrane_pomysly:
            st.warning("⚠️ Wybierz najpierw przynajmniej jeden pomysł z listy powyżej!")
        else:
            # Czyścimy starą galerię przed nowym malowaniem
            st.session_state.wygenerowane_obrazki = []
            
            # Tworzymy pusty kontener na podgląd generowanego obrazu
            kontener_podgladu = st.empty()
            
            for pomysl in wybrane_pomysly:
                st.subheader(f"🎨 Generuję: {pomysl.title}...")
                
                if not pomysl.visual_description.strip():
                    st.error("❌ Opis wizualny nie może być pusty! Uzupełnij go, aby wygenerować obraz.")
                    continue
                    
                for i in range(ilosc_rysunkow):
                    with st.spinner(f"Maluję wariant {i+1} dla: {pomysl.title}..."):
                        try:
                            # 1. API generuje
                            obrazek_odpowiedz = client.images.generate(
                                model="dall-e-3",
                                prompt=f"Czysty wektorowy line-art (lineart) w stylu dziecięcej książeczki do kolorowania. Absolutny zakaz używania jakichkolwiek kolorów, obraz musi być 100% monochromatyczny (tylko czarna linia i czyste białe tło, zero szarości). CAŁKOWITY ZAKAZ cieniowania, kropkowania (stippling) i gęstego kreskowania. Tylko grube, pojedyncze, wyraźne czarne kontury. Tematyka: {pomysl.visual_description}. Rysunek ma być dostosowany do wieku odbiorcy: {pomysl.recipient_age} lat. Poziom skomplikowania i trudności: {pomysl.difficulty}/5. Orientacyjna liczba głównych elementów na obrazku: {pomysl.number_of_elements}."
                            )

                            adres_obrazka = obrazek_odpowiedz.data[0].url
                            image_data = requests.get(adres_obrazka).content
                            
                            # Wyświetlamy obrazek w kontenerze podglądu natychmiast po namalowaniu
                            kontener_podgladu.image(image_data, caption=f"👀 Podgląd na żywo: {pomysl.title} (Wariant {i+1})")
                            
                            # 2. Wrzucamy do Session state
                            st.session_state.wygenerowane_obrazki.append({
                                "tytul": pomysl.title,
                                "wariant": i + 1,
                                "dane_bajty": image_data
                            })
                            
                        except Exception as e:
                            st.error(f"⚠️ Wystąpił błąd podczas generowania: {e}")
                            
            # Po zakończeniu pętli, czyścimy kontener, aby nie dublował Galerii na dole
            kontener_podgladu.empty()

    # GALERIA WYGENEROWANYCH OBRAZKÓW
    if st.session_state.wygenerowane_obrazki:
        st.divider()
        st.subheader("🖼️ Gotowe kolorowanki do pobrania:")
        
        for idx, img in enumerate(st.session_state.wygenerowane_obrazki):
            # Wyświetlamy z Session state
            st.image(img["dane_bajty"], caption=f"{img['tytul']} - Wariant {img['wariant']}")
            
            bezpieczny_tytul = img["tytul"].replace(' ', '_').replace('"', '')
            
            # Tworzymy guzik pobierania
            st.download_button(
                label=f"💾 Pobierz: {img['tytul']} (Wariant {img['wariant']})",
                data=img["dane_bajty"],
                file_name=f"kolorowanka_{bezpieczny_tytul}_wariant_{img['wariant']}.png",
                mime="image/png",
                key=f"dl_galeria_{idx}_{st.session_state.generation_id}"
            )

   