import streamlit as st

# Importăm modulele separate create de fiecare membru
import auth
import donator
import ong
import rapoarte

# Setări generale de pagină (Se pun doar în fișierul principal)
st.set_page_config(page_title="Platforma Donatii", layout="wide")

# Inițializăm fișierele de bază CSV (Funcție creată în auth.py de Membrul 1)
auth.init_fisiere()

# Inițializare variabile de sesiune pentru logare
if "logat" not in st.session_state:
    st.session_state["logat"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "rol" not in st.session_state:
    st.session_state["rol"] = ""

# Meniu de Navigare în Sidebar
st.sidebar.title("Meniu Navigare")
meniu = st.sidebar.radio("Alege Modulul:", 
                         ["1. Profil & Login", 
                          "2. Doneaza (Oferte)", 
                          "3. ONG (Cereri)", 
                          "4. Matching & Rapoarte"])

# Apelarea funcțiilor din fișierele colegilor în funcție de selecție
if meniu == "1. Profil & Login":
    auth.afiseaza_profil()

elif meniu == "2. Doneaza (Oferte)":
    donator.afiseaza_donator()

elif meniu == "3. ONG (Cereri)":
    ong.afiseaza_ong()

elif meniu == "4. Matching & Rapoarte":
    rapoarte.afiseaza_rapoarte()
