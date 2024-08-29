import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title('Orari di lavoro 2.0')
st.subheader('Ciao! Sono Poppo, con questa WebApp ti aiuto a formattare i tuoi orari di lavoro settimanali in una visualizzazione più comoda!')

# Aggiunta del campo per selezionare la data di inizio settimana
start_date = st.date_input("Seleziona il lunedì della settimana per cui stai pianificando gli orari:", 
                           min_value=datetime.now().date(), 
                           max_value=datetime.now().date() + timedelta(days=365))

# Assicuriamoci che la data selezionata sia un lunedì
while start_date.weekday() != 0:
    start_date -= timedelta(days=1)

st.markdown('Per ogni giorno della settimana seleziona orario di inizio e di fine.')
st.markdown('Se sei di RIPOSO basta che fai sì che i due orari coincidano, risultando in uno slider lungo 0.')
st.markdown('N.B.: Le mezze ore sono indicate come 0.5 negli slider.')

df_orari = pd.DataFrame(columns=['GIORNO', 'DATA', 'INIZIO', 'FINE'])

for i in range(7):
    current_date = start_date + timedelta(days=i)
    giorno = current_date.strftime("%A")
    data = current_date.strftime("%d %B")
    
    range = st.slider(f'Orario del {giorno} {data}:', 7.0, 23.0, [8.0, 22.0], 0.5)
    inizio = range[0]
    fine = range[1]
    
    inizio_str = f'{inizio:.2f}'.replace('.00', '.00').replace('.50', '.30')
    fine_str = f'{fine:.2f}'.replace('.00', '.00').replace('.50', '.30')
    
    if inizio == fine:
        inizio_str = 'RIPOSO'
        fine_str = 'RIPOSO'
    
    new_row = pd.DataFrame([[giorno, data, inizio_str, fine_str]], 
                           columns=['GIORNO', 'DATA', 'INIZIO', 'FINE'])
    df_orari = pd.concat([df_orari, new_row], ignore_index=True)

st.dataframe(df_orari, hide_index=True, use_container_width=True)

# Formattazione dell'output di testo
output_text = ""
for _, row in df_orari.iterrows():
    giorno = row['GIORNO']
    data = row['DATA']
    inizio = row['INIZIO']
    fine = row['FINE']
    
    output_text += f"{giorno} {data}\n"
    if inizio == 'RIPOSO':
        output_text += "RIPOSO\n"
    else:
        output_text += f"{inizio}  -  {fine}\n"
    output_text += "\n"

st.text(output_text)
