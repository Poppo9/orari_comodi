import streamlit as st
import pandas as pd
from tabulate import tabulate
settimana = ['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica']


st.title('Orari di lavoro 2.0')

st.subheader('Ciao! Sono Poppo, in questa webapp ti aiutereò a formattare i tuoi orari di lavoro settimanali \
             in diverse visualizzazioni più comode!')
st.markdown('Per ogni giorno della settimana seleziona orario di inzio e di fine, \
            se sei di RIPOSO basta che fai sì che i due orari coincidano, risultando in uno slider lungo 0.')
st.markdown('N.B.: Le mezze ore sono indicate come 0.5 negli slider.')
df_orari = pd.DataFrame(columns=['GIORNO','INIZIO','FINE'])
for giorno in settimana:
    range = st.slider(f'Orario del {giorno}:',7.0,23.0,[8.0,22.0],0.5)
    inizio = range[0]
    if inizio % 1 == 0.5:
        inizio = inizio - 0.2
    fine  = range[1]
    if fine % 1 == 0.5:
        fine = fine - 0.2
    
    inizio = f'{inizio:.2f}'

    fine = f'{fine:.2f}'

    if inizio == fine:
        inizio = 'RIPOSO'
        fine = 'RIPOSO'

    new_row = pd.DataFrame([[giorno, inizio, fine]], columns=['GIORNO', 'INIZIO', 'FINE'])
    df_orari = pd.concat([df_orari,new_row],ignore_index=True)
    #st.markdown(giorno)

st.dataframe(df_orari,hide_index= True,use_container_width=True)

st.text(tabulate(df_orari, headers='keys', tablefmt='list', showindex= False, floatfmt=".2f"))