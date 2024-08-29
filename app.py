import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

settimana = ['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica']

# Dizionario per la traduzione dei mesi
mesi_italiani = {
    1: 'gennaio', 2: 'febbraio', 3: 'marzo', 4: 'aprile',
    5: 'maggio', 6: 'giugno', 7: 'luglio', 8: 'agosto',
    9: 'settembre', 10: 'ottobre', 11: 'novembre', 12: 'dicembre'
}

st.title('Orari di lavoro 2.0')
st.subheader('Ciao! Sono Poppo, con questa WebApp ti aiuto a formattare i tuoi orari di lavoro settimanali in una visualizzazione più comoda!')

# Selezione della settimana
today = datetime.now()
start_of_current_week = today - timedelta(days=today.weekday())
selected_date = st.date_input(
    "Seleziona il lunedì della settimana desiderata:",
    start_of_current_week,
    key='date_selector'
)

# Assicurati che la data selezionata sia un lunedì
while selected_date.weekday() != 0:
    selected_date -= timedelta(days=1)

st.markdown('Per ogni giorno della settimana seleziona orario di inizio e di fine.')
st.markdown('Se sei di RIPOSO basta che fai sì che i due orari coincidano, risultando in uno slider lungo 0.')
st.markdown('N.B.: Le mezze ore sono indicate come 0.5 negli slider.')

df_orari = pd.DataFrame(columns=['GIORNO','INIZIO','FINE'])

# Funzione per formattare l'orario
def format_time(time):
    if time % 1 == 0.5:
        return f"{int(time):02d}.30"
    else:
        return f"{int(time):02d}.00"

# Funzione per formattare la data in italiano
def format_date_italian(date):
    return f"{date.day} {mesi_italiani[date.month]}"

for i, giorno in enumerate(settimana):
    current_date = selected_date + timedelta(days=i)
    date_str = format_date_italian(current_date)
    
    range = st.slider(f'Orario del {giorno} {date_str}:',7.0,23.0,[8.0,22.0],0.5)
    inizio = format_time(range[0])
    fine = format_time(range[1])
    
    if inizio == fine:
        inizio = 'RIPOSO'
        fine = 'RIPOSO'
    
    new_row = pd.DataFrame([[f"{giorno} {date_str}", inizio, fine]], columns=['GIORNO', 'INIZIO', 'FINE'])
    df_orari = pd.concat([df_orari,new_row],ignore_index=True)

st.dataframe(df_orari,hide_index=True,use_container_width=True)

# Formattazione personalizzata dell'output
output = ""
for _, row in df_orari.iterrows():
    output += f"{row['GIORNO']}\n"
    if row['INIZIO'] == 'RIPOSO':
        output += "RIPOSO\n"
    else:
        output += f"{row['INIZIO']}  -  {row['FINE']}\n"
    output += "\n"

st.text(output)
