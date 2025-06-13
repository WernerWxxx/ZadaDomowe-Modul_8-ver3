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


# import streamlit as st
# from dotenv import dotenv_values
# from openai import OpenAI
# from PIL import Image
# import base64
# import os

# st.set_page_config(page_title="Opis Obrazów", layout="centered")
# env = dotenv_values(".env")

# # if hasattr(st, "experimental_rerun"):
# #     st.experimental_rerun()
# # else:
# #     # Alternatywnie, można wymusić odświeżenie poprzez zmianę URL
# #     st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# # Funkcja do inicjalizacji klienta OpenAI
# def get_openai_client():
#     return OpenAI(api_key=st.session_state["openai_api_key"])

# # Funkcja do zapisania opisu do pliku tekstowego na dysku w wybranym katalogu
# def save_description_to_file(description_text, filename="images_descriptions.txt", directory="./saved_descriptions"):
#     try:
#         # Utwórz katalog, jeśli nie istnieje
#         os.makedirs(directory, exist_ok=True)
#         filepath = os.path.join(directory, filename)
#         with open(filepath, "a", encoding="utf-8") as f:
#             f.write(description_text + "\n")
#         st.success(f"Opis zapisany do pliku {filepath}")
#     except Exception as e:
#         st.error(f"Błąd zapisu do pliku: {e}")
# # # 1 ver
# # # Funkcja do zapisania opisu do pliku tekstowego na dysku
# # def save_description_to_file(description_text, filename="descriptions.txt"):
# #     try:
# #         with open(filename, "a", encoding="utf-8") as f:
# #             f.write(description_text + "\n")
# #         st.success(f"Opis zapisany do pliku {filename}")
# #     except Exception as e:
# #         st.error(f"Błąd zapisu do pliku: {e}")

# # Inicjalizacja kluczy w session_state
# if "openai_api_key" not in st.session_state:
#     st.session_state["openai_api_key"] = env.get("OPENAI_API_KEY", "")

# # Pobieranie klucza API OpenAI
# if not st.session_state.get("openai_api_key"):
#     if "OPENAI_API_KEY" in env:
#         st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
#     else:
#         st.info("Dodaj swój klucz API OpenAI, aby korzystać z tej aplikacji")
#         st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
#         if st.session_state["openai_api_key"]:
#             #st.experimental_rerun()
#             st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# if not st.session_state["openai_api_key"]:
#     st.stop()

# st.title("Opis Obrazów")

# uploaded_file = st.file_uploader("Wybierz obraz", type=["PNG", "JPG", "JPEG"])

# if uploaded_file is not None:
#     # Wyświetlenie obrazu
#     image_bytes = uploaded_file.read()
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Załadowany obraz', use_container_width=True)

#     # Funkcja do generowania opisu
#     def generate_description(image_bytes):
#         openai_client = get_openai_client()
#         image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#         response = openai_client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "Opisz ten obraz."},
#                 {"role": "user", "content": f"Proszę opisać obraz o kodzie base64: {image_base64}"}
#             ],
#         )
#         description = response.choices[0].message.content
#         return description

#     # Generowanie opisu po kliknięciu przycisku
#     if st.button("Generuj opis"):
#         description_text = generate_description(image_bytes)
#         st.session_state["description_text"] = description_text

#     # Pole tekstowe do edycji opisu
#     if "description_text" in st.session_state:
#         st.session_state["description_text"] = st.text_area(
#             "Edytuj opis", value=st.session_state.get("description_text", "")
#         )
#         # później w kodzie, przy zapisie:
#     #if st.session_state.get("description_text"):
#     if st.button("Zapisz opis do pliku"):
#         save_description_to_file(
#             st.session_state["description_text"],
#             filename="images_descriptions.txt",
#             directory="./saved_descriptions"
#         )
#         st.toast("Opis zapisany do pliku", icon="🎉")


    
#     # # Przycisk do zapisu opisu do pliku
#     # if st.session_state.get("description_text"):
#     #     if st.button("Zapisz opis do pliku"):
#     #         save_description_to_file(st.session_state["description_text"])
#     #         st.toast("Opis zapisany do pliku", icon="🎉")




#---3
# import streamlit as st
# from dotenv import dotenv_values
# from openai import OpenAI
# from PIL import Image
# import base64

# st.set_page_config(page_title="Opis Obrazów", layout="centered")
# env = dotenv_values(".env")

# # if hasattr(st, "experimental_rerun"):
# #     st.experimental_rerun()
# # else:
# #     # Alternatywnie, można wymusić odświeżenie poprzez zmianę URL
# #     st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# # Funkcja do inicjalizacji klienta OpenAI
# def get_openai_client():
#     return OpenAI(api_key=st.session_state["openai_api_key"])

# # Funkcja do zapisania opisu do wybranego pliku tekstowego
# def save_description_to_file(description_text, filename="descriptions.txt"):
#     try:
#         with open(filename, "a", encoding="utf-8") as f:
#             f.write(description_text + "\n")
#         st.success(f"Opis zapisany do pliku {filename}")
#     except Exception as e:
#         st.error(f"Błąd zapisu do pliku: {e}")

# # Funkcja do odczytu zawartości pliku tekstowego (opcjonalnie)
# def load_descriptions_from_file(filename):
#     try:
#         with open(filename, "r", encoding="utf-8") as f:
#             return f.read()
#     except Exception:
#         return ""

# # Inicjalizacja kluczy w session_state
# if "openai_api_key" not in st.session_state:
#     st.session_state["openai_api_key"] = env.get("OPENAI_API_KEY", "")

# # Pobieranie klucza API OpenAI
# if not st.session_state.get("openai_api_key"):
#     if "OPENAI_API_KEY" in env:
#         st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
#     else:
#         st.info("Dodaj swój klucz API OpenAI, aby korzystać z tej aplikacji")
#         st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
#         if st.session_state["openai_api_key"]:
#             #st.experimental_rerun()
#             st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# if not st.session_state["openai_api_key"]:
#     st.stop()

# st.title("Opis Obrazów")

# # Dodanie widgetu do wyboru pliku tekstowego
# txt_file = st.file_uploader("Wybierz plik tekstowy do zapisu opisów", type=["txt"])

# # Jeśli plik został wybrany, można go odczytać (opcjonalnie)
# if txt_file is not None:
#     # Odczyt zawartości pliku i wyświetlenie (np. wcześniejszych opisów)
#     descriptions_content = load_descriptions_from_file(txt_file)
#     st.write("Zawartość pliku:")
#     st.text_area("Wcześniejsze opisy", value=descriptions_content, height=200)

# uploaded_file = st.file_uploader("Wybierz obraz", type=["PNG", "JPG", "JPEG"])

# if uploaded_file is not None:
#     # Wyświetlenie obrazu
#     image_bytes = uploaded_file.read()
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Załadowany obraz', use_container_width=True)

#     # Funkcja do generowania opisu
#     def generate_description(image_bytes):
#         openai_client = get_openai_client()
#         image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#         response = openai_client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "Opisz ten obraz."},
#                 {"role": "user", "content": f"Proszę opisać obraz o kodzie base64: {image_base64}"}
#             ],
#         )
#         description = response.choices[0].message.content
#         return description

#     # Generowanie opisu po kliknięciu przycisku
#     if st.button("Generuj opis"):
#         description_text = generate_description(image_bytes)
#         st.session_state["description_text"] = description_text

#     # Pole tekstowe do edycji opisu
#     if "description_text" in st.session_state:
#         st.session_state["description_text"] = st.text_area(
#             "Edytuj opis", value=st.session_state.get("description_text", "")
#         )

#     # Przycisk do zapisu opisu do pliku
#     if st.session_state.get("description_text"):
#         if st.button("Zapisz opis do wybranego pliku"):
#             # Sprawdzenie czy wybrano plik tekstowy
#             if txt_file is not None:
#                 filename = txt_file.name
#             else:
#                 filename = "descriptions.txt"  # domyślny plik

#             save_description_to_file(st.session_state["description_text"], filename=filename)
#             st.toast("Opis zapisany do pliku", icon="🎉")
#---2
# import streamlit as st
# from dotenv import dotenv_values
# from openai import OpenAI
# from PIL import Image
# import base64

# st.set_page_config(page_title="Opis Obrazów", layout="centered")
# env = dotenv_values(".env")

# # Funkcja do inicjalizacji klienta OpenAI
# def get_openai_client():
#     return OpenAI(api_key=st.session_state["openai_api_key"])

# # Funkcja do zapisania opisu do pliku tekstowego na dysku
# def save_description_to_file(description_text, filename="descriptions.txt"):
#     try:
#         with open(filename, "a", encoding="utf-8") as f:
#             f.write(description_text + "\n")
#         st.success(f"Opis zapisany do pliku {filename}")
#     except Exception as e:
#         st.error(f"Błąd zapisu do pliku: {e}")

# # Inicjalizacja kluczy w session_state
# if "openai_api_key" not in st.session_state:
#     st.session_state["openai_api_key"] = env.get("OPENAI_API_KEY", "")

# # Pobieranie klucza API OpenAI
# if not st.session_state.get("openai_api_key"):
#     if "OPENAI_API_KEY" in env:
#         st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
#     else:
#         st.info("Dodaj swój klucz API OpenAI, aby korzystać z tej aplikacji")
#         st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
#         if st.session_state["openai_api_key"]:
#             st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# if not st.session_state["openai_api_key"]:
#     st.stop()

# st.title("Opis Obrazów")

# # Wybór pliku tekstowego do zapisu opisów
# st.write("Wybierz plik tekstowy do zapisywania opisów (opcjonalnie):")
# txt_file_upload = st.file_uploader("Wybierz plik txt", type=["txt"])

# # Ustal nazwę pliku do zapisu
# if txt_file_upload is not None:
#     # Jeśli użytkownik wybrał plik, zapisz go na dysk i korzystaj z tego pliku
#     # Aby odczytać zawartość, najpierw zapisujemy go do tymczasowego pliku lokalnego
#     import tempfile
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
#     temp_file.write(txt_file_upload.read())
#     temp_file.close()
#     save_filename = temp_file.name
# else:
#     # Domyślny plik
#     save_filename = "descriptions.txt"

# uploaded_file = st.file_uploader("Wybierz obraz", type=["PNG", "JPG", "JPEG"])

# if uploaded_file is not None:
#     # Wyświetlenie obrazu
#     image_bytes = uploaded_file.read()
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Załadowany obraz', use_container_width=True)

#     # Funkcja do generowania opisu
#     def generate_description(image_bytes):
#         openai_client = get_openai_client()
#         image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#         response = openai_client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "Opisz ten obraz."},
#                 {"role": "user", "content": f"Proszę opisać obraz o kodzie base64: {image_base64}"}
#             ],
#         )
#         description = response.choices[0].message.content
#         return description

#     # Generowanie opisu po kliknięciu przycisku
#     if st.button("Generuj opis"):
#         description_text = generate_description(image_bytes)
#         st.session_state["description_text"] = description_text

#     # Pole tekstowe do edycji opisu
#     if "description_text" in st.session_state:
#         st.session_state["description_text"] = st.text_area(
#             "Edytuj opis", value=st.session_state.get("description_text", "")
#         )

#     # Przycisk do zapisu opisu do pliku
#     if st.session_state.get("description_text"):
#         if st.button("Zapisz opis do pliku"):
#             save_description_to_file(st.session_state["description_text"], filename=save_filename)
#             st.toast("Opis zapisany do pliku", icon="🎉")

#---1

# import streamlit as st
# from dotenv import dotenv_values
# from openai import OpenAI
# from PIL import Image
# import base64

# st.set_page_config(page_title="Opis Obrazów", layout="centered")
# env = dotenv_values(".env")

# # if hasattr(st, "experimental_rerun"):
# #     st.experimental_rerun()
# # else:
# #     # Alternatywnie, można wymusić odświeżenie poprzez zmianę URL
# #     st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# # Funkcja do inicjalizacji klienta OpenAI
# def get_openai_client():
#     return OpenAI(api_key=st.session_state["openai_api_key"])

# # Funkcja do zapisania opisu do pliku tekstowego na dysku
# def save_description_to_file(save_filename, filename="save_filename"):
#     try:
#         with open(filename, "a", encoding="utf-8") as f:
#             f.write(save_filename + "\n")
#         st.success(f"Opis zapisany do pliku {filename}")
#     except Exception as e:
#         st.error(f"Błąd zapisu do pliku: {e}")

# # Inicjalizacja kluczy w session_state
# if "openai_api_key" not in st.session_state:
#     st.session_state["openai_api_key"] = env.get("OPENAI_API_KEY", "")

# # Pobieranie klucza API OpenAI
# if not st.session_state.get("openai_api_key"):
#     if "OPENAI_API_KEY" in env:
#         st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
#     else:
#         st.info("Dodaj swój klucz API OpenAI, aby korzystać z tej aplikacji")
#         st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
#         if st.session_state["openai_api_key"]:
#             #st.experimental_rerun()
#             st.write("<script>window.location.reload();</script>", unsafe_allow_html=True)

# if not st.session_state["openai_api_key"]:
#     st.stop()

# st.title("Opis Obrazów")

# #///
# # Wybór pliku tekstowego do zapisu opisów
# st.write("Wybierz plik tekstowy do zapisywania opisów (opcjonalnie):")
# txt_file_upload = st.file_uploader("Wybierz plik txt", type=["txt"])

# # Ustal nazwę pliku do zapisu
# if txt_file_upload is not None:
#     # Jeśli użytkownik wybrał plik, zapisz go na dysk i korzystaj z tego pliku
#     # Aby odczytać zawartość, najpierw zapisujemy go do tymczasowego pliku lokalnego
#     import tempfile
#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
#     temp_file.write(txt_file_upload.read())
#     temp_file.close()
#     save_filename = temp_file.name
# # else:
# #     # Domyślny plik
# #     save_filename = "descriptions.txt"
# #///

# uploaded_file = st.file_uploader("Wybierz obraz", type=["PNG", "JPG", "JPEG"])

# if uploaded_file is not None:
#     # Wyświetlenie obrazu
#     image_bytes = uploaded_file.read()
#     image = Image.open(uploaded_file)
#     st.image(image, caption='Załadowany obraz', use_container_width=True)

#     # Funkcja do generowania opisu
#     def generate_description(image_bytes):
#         openai_client = get_openai_client()
#         image_base64 = base64.b64encode(image_bytes).decode('utf-8')
#         response = openai_client.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "Opisz ten obraz."},
#                 {"role": "user", "content": f"Proszę opisać obraz o kodzie base64: {image_base64}"}
#             ],
#         )
#         description = response.choices[0].message.content
#         return description

#     # Generowanie opisu po kliknięciu przycisku
#     if st.button("Generuj opis"):
#         save_filename = generate_description(image_bytes)
#         st.session_state["save_filename"] = save_filename
#         #description_text = generate_description(image_bytes)
#         #st.session_state["description_text"] = description_text

#     # Pole tekstowe do edycji opisu
#     if "save_filename" in st.session_state:
#         st.session_state["description_text"] = st.text_area(
#             "Edytuj opis", value=st.session_state.get("description_text", "")
#         )

#     # Przycisk do zapisu opisu do pliku
#     if st.session_state.get("save_filename"):
#     #if st.session_state.get("description_text"):
#         if st.button("Zapisz opis do pliku"):
#             save_description_to_file(st.session_state["save_filename"])
#             st.toast("Opis zapisany do pliku", icon="🎉")
#             #save_description_to_file(st.session_state["description_text"])
#             #st.toast("Opis zapisany do pliku", icon="🎉")
