import streamlit as st
import pandas as pd

FISIER_DONATII = 'donatii.csv'
FISIER_CERERI = 'cereri.csv'

def afiseaza_rapoarte():
    st.header("Motor de Matching si Statistici")
    
    df_donatii = pd.read_csv(FISIER_DONATII)
    df_cereri = pd.read_csv(FISIER_CERERI)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Obiecte Donate", len(df_donatii))
    col2.metric("Total Cereri Lansate", len(df_cereri))
    
    st.markdown("---")
    st.subheader("Potriviri Automate (Matching)")
    st.info("Sistemul compara tabelele CSV pentru a gasi cereri si oferte din aceeasi categorie.")
    
    if not df_cereri.empty and not df_donatii.empty:
        donatii_disponibile = df_donatii[df_donatii['status'] == 'Disponibil']
        
        # Combinarea tabelelor pe baza aceleiași categorii
        df_matching = pd.merge(
            df_cereri, 
            donatii_disponibile, 
            on='categorie', 
            how='inner', 
            suffixes=('_Cerere', '_Oferta')
        )
        
        if not df_matching.empty:
            tabel_afisare = df_matching[['beneficiar', 'descriere_Cerere', 'donator', 'descriere_Oferta', 'categorie']]
            tabel_afisare.columns = ['ONG / Beneficiar', 'Ce se cere', 'Donator gasit', 'Ce se ofera', 'Categorie']
            
            st.dataframe(tabel_afisare, use_container_width=True)
            
            csv = tabel_afisare.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descarca Lista de Distributie (CSV)",
                data=csv,
                file_name='lista_distributie_matching.csv',
                mime='text/csv',
            )
        else:
            st.write("Nu s-au gasit potriviri exacte momentan.")
    else:
        st.write("Nu exista suficiente date in fisiere pentru a face matching.")

    st.markdown("---")
    st.subheader("Analiza Categorii (Din fisierul donatii.csv)")
    
    if not df_donatii.empty:
        st.bar_chart(df_donatii['categorie'].value_counts())
