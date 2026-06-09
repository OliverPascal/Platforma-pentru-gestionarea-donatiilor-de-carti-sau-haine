import streamlit as st
import pandas as pd

FISIER_DONATII = 'donatii.csv'

def afiseaza_donator():
    st.header("Ofera o Donatie")
    #doar utilizatorii logati ca "Donator" au acces la acest modul
    if st.session_state["logat"] and st.session_state["rol"] == "Donator":
        # utilizam un formular pentru a colecta datele simultan, clear_on_submit curața automat interfata dupa o adaugare 
        with st.form("form_donatie", clear_on_submit=True):
            st.subheader("Adauga un obiect nou")
            categorie = st.selectbox("Categorie", ["Carti", "Haine", "Jucarii"])
            descriere = st.text_input("Descriere (ex: Geaca iarna M, Culegere Mate clasa 8)")
            stare = st.radio("Stare", ["Nou", "Purtat/Folosit", "Necesita reparatii"])
            submit = st.form_submit_button("Inregistreaza Donatia")
            
            #se proceseaza datele doar daca butonul a fost apasat si descrierea nu e goala
            if submit and descriere:
                #incarcare date existente pentru actualizare
                df_donatii = pd.read_csv(FISIER_DONATII)
                noul_id = len(df_donatii) + 1
                
                #creare DataFrame cu datele din formular
                noua_donatie = pd.DataFrame([{
                    'id': noul_id, 'donator': st.session_state["username"], 
                    'categorie': categorie, 'descriere': descriere, 
                    'stare': stare, 'status': 'Disponibil'
                }])

                # adugarea noii înregistrari ai salvarea în fisierul CSV
                df_donatii = pd.concat([df_donatii, noua_donatie], ignore_index=True)
                df_donatii.to_csv(FISIER_DONATII, index=False)
                st.success("Obiectul a fost adaugat in stoc!")

        st.markdown("---")
        st.subheader("Istoricul Donatiilor Tale")
        
        #reincarcam datele din fisier pentru a actualiza tabelul de pe ecran
        df_donatii = pd.read_csv(FISIER_DONATII)
        
        #pastram doar randurile cu donatiile facute de utilizatorul conectat acum
        donatiile_mele = df_donatii[df_donatii['donator'] == st.session_state['username']]

        #afisam tabelul final
        st.dataframe(donatiile_mele[['categorie', 'descriere', 'stare', 'status']], use_container_width=True)
    else:
        st.warning("Trebuie sa fii logat ca Donator pentru a accesa aceasta pagina.")
