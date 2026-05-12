# 🎨 AI Generator Kolorowanek

Interaktywna aplikacja webowa zbudowana w Streamlit, która pozwala na generowanie spersonalizowanych, wektorowych kolorowanek dla dzieci. Wykorzystuje modele językowe do tworzenia szczegółowych opisów (promptów) oraz model DALL-E 3 do generowania obrazów w ściśle określonym, monochromatycznym stylu.

🌐 **[Przetestuj aplikację na żywo w Streamlit Cloud](https://appcoloringbooks-fh01.streamlit.app/)** *(Uwaga: Ze względów bezpieczeństwa i limitów API, do przetestowania generatora na żywo wymagane jest podanie własnego klucza OpenAI API).*

---

## ✨ Główne funkcjonalności

* **Inteligentne generowanie pomysłów:** Wykorzystanie modelu LLM (wspieranego przez biblioteki `instructor` i `Pydantic`) do strukturyzowanego generowania kreatywnych tytułów i precyzyjnych opisów wizualnych na podstawie prostego hasła podanego przez użytkownika.
* **Zarządzanie stanem (Session State):** Aplikacja bezpiecznie przechowuje wygenerowane pomysły i obrazy w pamięci sesji, zapobiegając ich utracie podczas przeładowań interfejsu (np. przy kliknięciu w przycisk).
* **Zapis i odczyt sesji (JSON):** Mechanizm pobierania obecnej historii pomysłów na dysk twardy (w formacie `.json`) oraz wczytywania jej z powrotem do aplikacji w dowolnym momencie.
* **Podgląd na żywo:** Dynamiczny kontener informacyjny, który wyświetla generowane grafiki w czasie rzeczywistym, zanim trafią one do ostatecznej, głównej galerii.
* **Pobieranie plików PNG:** System łatwego i bezpiecznego pobierania pojedynczych wariantów wygenerowanych obrazków z automatycznie formatowanymi, unikalnymi nazwami plików.
* **Architektura BYOK (Bring Your Own Key):** Bezpieczne zarządzanie uwierzytelnianiem. Aplikacja nie przechowuje globalnych kluczy na serwerze i inteligentnie weryfikuje ich obecność (lub prosi o ich podanie) przed odblokowaniem interfejsu.

---

## 🛠 Technologie i biblioteki

Aplikacja została zbudowana w oparciu o nowoczesny stos technologiczny Pythona:

* **Język:** Python 3.11
* **Frontend / Interfejs:** `streamlit`
* **Silnik AI:** `openai` (API: gpt-3.5-turbo / gpt-4o, dall-e-3)
* **Strukturyzacja i walidacja danych:** `pydantic`, `instructor`
* **Obsługa zmiennych i sieci:** `python-dotenv` (do obsługi plików .env), `requests` (do pobierania obrazów z serwerów OpenAI do pamięci).

---
