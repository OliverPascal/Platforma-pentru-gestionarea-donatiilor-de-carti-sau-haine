import streamlit as st #Biblioteca Streamlit este folosita pentru a crea butoane, formulare si tabele direct in Python
import pandas as pd    #Biblioteca Pandas este esentiala pentru citirea, modificarea si salvarea tabelelor de date

FISIER_CERERI = 'cereri.csv'  #O constanta care retine numele fisierului CSV  unde stocam toate cererile ONG-urilor

def afiseaza_ong():
    st.header("Catalog si Cereri")

    #Norma de securitate:
    if st.session_state["logat"] and st.session_state["rol"] == "ONG / Beneficiar":

        #Grupeaza elementele intr-un formular
        with st.form("form_cerere", clear_on_submit=True):
            st.subheader("Ce aveti nevoie?")
            cat_cerere = st.selectbox("Categorie cautata", ["Carti", "Haine", "Jucarii"])
            desc_cerere = st.text_input("Descrieti necesarul (ex: 20 de perechi de ghete marimea 40)")
            submit_cerere = st.form_submit_button("Lanseaza Cererea")

            #Salvarea efectiva a datelor
            if submit_cerere and desc_cerere:
                df_cereri = pd.read_csv(FISIER_CERERI)
                noul_id = len(df_cereri) + 1
                noua_cerere = pd.DataFrame([{
                    'id': noul_id, 'beneficiar': st.session_state["username"], 
                    'categorie': cat_cerere, 'descriere': desc_cerere, 'status': 'In asteptare'
                }])
                df_cereri = pd.concat([df_cereri, noua_cerere], ignore_index=True)
                df_cereri.to_csv(FISIER_CERERI, index=False)
                st.success("Cererea a fost inregistrata!")

        #Structura pentru noua cerere
        st.markdown("---")
        st.subheader("Cererile tale active")
        df_cereri = pd.read_csv(FISIER_CERERI)
        cererile_mele = df_cereri[df_cereri['beneficiar'] == st.session_state['username']]
        st.dataframe(cererile_mele[['categorie', 'descriere', 'status']], use_container_width=True)
    else:
        st.warning("Trebuie sa fii logat ca ONG / Beneficiar pentru a accesa aceasta pagina.")
