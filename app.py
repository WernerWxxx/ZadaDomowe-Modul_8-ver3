import streamlit as st
from dotenv import dotenv_values
from openai import OpenAI
from PIL import Image
import base64
import os
from datetime import datetime

st.set_page_config(page_title="Opis Obrazów", layout="centered")
env = dotenv_values(".env")

# Funkcja do inicjalizacji klienta OpenAI
def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])

# Funkcja do zapisywania opisu do pliku w wybranym katalogu
def save_description_to_file(description_text, directory, filename=None):
    try:
        # Jeśli nazwa pliku nie jest podana, generujemy ją na podstawie czasu
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"description_{timestamp}.txt"
        # Tworzymy pełną ścieżkę do pliku
        filepath = os.path.join(directory, filename)
        # Upewniamy się, że katalog istnieje
        os.makedirs(directory, exist_ok=True)
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(description_text + "\n")
        st.success(f"Opis zapisany do pliku {filepath}")
    except Exception as e:
        st.error(f"Błąd zapisu do pliku: {e}")

# Inicjalizacja kluczy w session_state
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = env.get("OPENAI_API_KEY", "")

# Pobieranie klucza API OpenAI
if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
    else:
        st.info("Dodaj swój klucz API OpenAI, aby korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

if not st.session_state["openai_api_key"]:
    st.stop()

st.title("Opis Obrazów")

# Dodajemy wybór katalogu do zapisu
st.sidebar.header("Ustawienia zapisu")
save_directory = st.sidebar.text_input("Podaj ścieżkę katalogu do zapisu", value="obrazowe_opisy")
# Opcjonalnie można dodać wybór folderu z poziomu systemu plików, ale Streamlit na to nie pozwala bez dodatkowych bibliotek

uploaded_file = st.file_uploader("Wybierz obraz", type=["PNG", "JPG", "JPEG"])

if uploaded_file is not None:
    # Wyświetlenie obrazu
    image_bytes = uploaded_file.read()
    image = Image.open(uploaded_file)
    st.image(image, caption='Załadowany obraz', use_container_width=True)

    # Funkcja do generowania opisu
    def generate_description(image_bytes):
        openai_client = get_openai_client()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Opisz ten obraz."},
                {"role": "user", "content": f"Proszę opisać obraz o kodzie base64: {image_base64}"}
            ],
        )
        description = response.choices[0].message.content
        return description

    # Generowanie opisu po kliknięciu przycisku
    if st.button("Generuj opis"):
        description_text = generate_description(image_bytes)
        st.session_state["description_text"] = description_text

    # Pole tekstowe do edycji opisu
    if "description_text" in st.session_state:
        st.session_state["description_text"] = st.text_area(
            "Edytuj opis", value=st.session_state.get("description_text", "")
        )

    # Przycisk do zapisu opisu do pliku w wybranym katalogu
    if st.session_state.get("description_text"):
        if st.button("Zapisz opis do pliku"):
            save_description_to_file(
                st.session_state["description_text"],
                directory=save_directory
            )
            st.toast("Opis zapisany do pliku", icon="🎉")