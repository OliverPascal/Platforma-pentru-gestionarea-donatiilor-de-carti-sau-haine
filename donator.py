import streamlit as st
import pandas as pd

FISIER_DONATII = 'donatii.csv'

def afiseaza_donator():
    st.header("Ofera o Donatie")
    
    if st.session_state["logat"] and st.session_state["rol"] == "Donator":
        with st.form("form_donatie", clear_on_submit=True):
            st.subheader("Adauga un obiect nou")
            categorie = st.selectbox("Categorie", ["Carti", "Haine", "Jucarii"])
            descriere = st.text_input("Descriere (ex: Geaca iarna M, Culegere Mate clasa 8)")
            stare = st.radio("Stare", ["Nou", "Purtat/Folosit", "Necesita reparatii"])
            submit = st.form_submit_button("Inregistreaza Donatia")
            
            if submit and descriere:
                df_donatii = pd.read_csv(FISIER_DONATII)
                noul_id = len(df_donatii) + 1
                noua_donatie = pd.DataFrame([{
                    'id': noul_id, 'donator': st.session_state["username"], 
                    'categorie': categorie, 'descriere': descriere, 
                    'stare': stare, 'status': 'Disponibil'
                }])
                df_donatii = pd.concat([df_donatii, noua_donatie], ignore_index=True)
                df_donatii.to_csv(FISIER_DONATII, index=False)
                st.success("Obiectul a fost adaugat in stoc!")

        st.markdown("---")
        st.subheader("Istoricul Donatiilor Tale")
        df_donatii = pd.read_csv(FISIER_DONATII)
        donatiile_mele = df_donatii[df_donatii['donator'] == st.session_state['username']]
        st.dataframe(donatiile_mele[['categorie', 'descriere', 'stare', 'status']], use_container_width=True)
    else:
        st.warning("Trebuie sa fii logat ca Donator pentru a accesa aceasta pagina.")
