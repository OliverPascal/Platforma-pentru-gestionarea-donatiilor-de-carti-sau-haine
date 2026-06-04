import streamlit as st
import pandas as pd
import os

FISIER_USERI = 'utilizatori.csv'
FISIER_DONATII = 'donatii.csv'
FISIER_CERERI = 'cereri.csv'

# Funcție care creează fișierele CSV automat dacă ele nu există
def init_fisiere():
    if not os.path.exists(FISIER_USERI):
        pd.DataFrame(columns=['username', 'parola', 'rol']).to_csv(FISIER_USERI, index=False)
    if not os.path.exists(FISIER_DONATII):
        pd.DataFrame(columns=['id', 'donator', 'categorie', 'descriere', 'stare', 'status']).to_csv(FISIER_DONATII, index=False)
    if not os.path.exists(FISIER_CERERI):
        pd.DataFrame(columns=['id', 'beneficiar', 'categorie', 'descriere', 'status']).to_csv(FISIER_CERERI, index=False)

# Funcția principală a modulului
def afiseaza_profil():
    st.header("Autentificare si Cont")
    
    if not st.session_state["logat"]:
        tab_login, tab_register = st.tabs(["Login", "Creeaza Cont"])
        
        with tab_login:
            user_login = st.text_input("Nume utilizator (Login)")
            pass_login = st.text_input("Parola (Login)", type="password")
            if st.button("Logheaza-te"):
                df_useri = pd.read_csv(FISIER_USERI)
                user_gasit = df_useri[(df_useri['username'] == user_login) & (df_useri['parola'] == pass_login)]
                
                if not user_gasit.empty:
                    st.session_state["logat"] = True
                    st.session_state["username"] = user_login
                    st.session_state["rol"] = user_gasit.iloc[0]['rol']
                    st.success("Te-ai logat cu succes!")
                    st.rerun()
                else:
                    st.error("Utilizator sau parola incorecte!")
                    
        with tab_register:
            user_reg = st.text_input("Nume utilizator (Cont nou)")
            pass_reg = st.text_input("Parola", type="password")
            rol_reg = st.selectbox("Rolul tau:", ["Donator", "ONG / Beneficiar"])
            if st.button("Creeaza cont"):
                df_useri = pd.read_csv(FISIER_USERI)
                if user_reg in df_useri['username'].values:
                    st.error("Numele de utilizator exista deja.")
                else:
                    nou_user = pd.DataFrame([{'username': user_reg, 'parola': pass_reg, 'rol': rol_reg}])
                    df_useri = pd.concat([df_useri, nou_user], ignore_index=True)
                    df_useri.to_csv(FISIER_USERI, index=False)
                    st.success("Cont creat cu succes! Te poti loga acum din sectiunea Login.")
    else:
        st.success(f"Esti logat ca: **{st.session_state['username']}** (Rol: {st.session_state['rol']})")
        if st.button("Deconectare"):
            st.session_state["logat"] = False
            st.session_state["username"] = ""
            st.session_state["rol"] = ""
            st.rerun()
