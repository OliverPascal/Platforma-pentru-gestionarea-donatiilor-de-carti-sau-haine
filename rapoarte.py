elif meniu == "4. Matching & Rapoarte":
    st.header(" Motor de Matching și Statistici")
    
    df_donatii = pd.read_csv(FISIER_DONATII)
    df_cereri = pd.read_csv(FISIER_CERERI)
    
    # Statistici Generale
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Obiecte Donate", len(df_donatii))
    col2.metric("Total Cereri Lansate", len(df_cereri))
    
    st.markdown("---")
    st.subheader(" Potriviri Automate (Matching)")
    st.info("Sistemul compară tabelele CSV pentru a găsi cereri și oferte din aceeași categorie.")
    
    # Algoritm de matching folosind Pandas Merge în loc de SQL JOIN
    if not df_cereri.empty and not df_donatii.empty:
        donatii_disponibile = df_donatii[df_donatii['status'] == 'Disponibil']
        
        # Facem un JOIN (merge) intern pe coloana 'categorie'
        df_matching = pd.merge(
            df_cereri, 
            donatii_disponibile, 
            on='categorie', 
            how='inner', 
            suffixes=('_Cerere', '_Oferta')
        )
        
        if not df_matching.empty:
            # Aranjăm coloanele frumos pentru afișare
            tabel_afisare = df_matching[['beneficiar', 'descriere_Cerere', 'donator', 'descriere_Oferta', 'categorie']]
            tabel_afisare.columns = ['ONG / Beneficiar', 'Ce se cere', 'Donator găsit', 'Ce se oferă', 'Categorie']
            
            st.dataframe(tabel_afisare, use_container_width=True)
            
            # Export Listă Distribuție
            csv = tabel_afisare.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=" Descarcă Lista de Distribuție (CSV)",
                data=csv,
                file_name='lista_distributie_matching.csv',
                mime='text/csv',
            )
        else:
            st.write("Nu s-au găsit potriviri exacte momentan.")
    else:
        st.write("Nu există suficiente date în fișiere pentru a face matching.")

    st.markdown("---")
    st.subheader("Analiză Categorii (Din fișierul donatii.csv)")
    
    if not df_donatii.empty:
        st.bar_chart(df_donatii['categorie'].value_counts())
