import streamlit as st
import requests
import json
import pandas as pd

docker_url = "http://localhost:5000/predict"
df = pd.read_csv('../data/feature_data/map_comuni_regioni.csv')

st.markdown('''
    # Welcome to your Price Prediction Assistant!
    Through the graphic interface below, you can provide information on your house and I will predict what its selling price should be!
    
    *Note: My predictions are not 100% accurate so always take them with a grain of salt* 
    ''')

new_input_dict = {}

new_input_dict['bagni'] = st.pills('Bathrooms', ['1', '2', '3', '3+'])
new_input_dict['stanze'] = st.pills('Bedrooms', ['1', '2', '3', '4', '5', '5+'])
new_input_dict['camere'] = int(new_input_dict['stanze'])  
new_input_dict['disponibilità'] = st.pills('Availability', ['Libero', 'Futuro', 'missing'])
new_input_dict['locali'] = st.pills('Rooms', ['1', '2', '3', '4', '5', '5+'], key='Rooms')
new_input_dict['cucina'] = st.pills('Kitchen',['cucina abitabile', 'cucina semi abitabile','cucina angolo cottura', 'cucina a vista', 'no info','cucina cucinotto'])
new_input_dict['tipologia_casa'] = st.selectbox('House Type', ['Appartamento','Appartamento in villa','Attico','Baglio','Baita','Casa colonica','Casale','Cascina','Chalet','Dammuso','Loft','Mansarda','Open space','Palazzo - Edificio','Rustico','Sasso','Terratetto plurifamiliare','Terratetto unifamiliare','Villa a schiera','Villa bifamiliare','Villa plurifamiliare','Villa unifamiliare']) 
new_input_dict['classe_casa'] = st.pills('House Class', ['Classe immobile economica','Classe immobile media','Classe immobile signorile','Immobile di lusso','Sconosciuta'])
new_input_dict['classe_casa'] = 'missing' if new_input_dict['classe_casa']=='Sconosciuta' else new_input_dict['classe_casa']
new_input_dict['tipologia_proprietà'] = st.pills('Property Type', ['Diritto di superficie','Intera proprietà','Multiproprietà','Nuda proprietà','Parziale proprietà','Sconosciuta'])
new_input_dict['tipologia_proprietà'] = 'missing' if new_input_dict['tipologia_proprietà']=='Sconosciuta' else new_input_dict['tipologia_proprietà']
new_input_dict['giardino'] = st.pills('Giardino', ['comune','privato','assente'])
new_input_dict['giardino'] = 'Missing' if new_input_dict['giardino']=='assente' else new_input_dict['giardino']
new_input_dict['infissi'] = st.pills('Tipologia Infissi', ['singolo','doppio','triplo', 'sconosciuto'])
new_input_dict['infissi'] = 'missing' if new_input_dict['infissi']=='sconosciuto' else new_input_dict['infissi']
new_input_dict['piano'] = st.number_input('Piano (digitare -1 se non applicabile o sconosciuto)', min_value=-1)
new_input_dict['totale_piani'] = st.number_input('Totale piani (digitare -1 se non applicabile o sconosciuto)', min_value=-1)
new_input_dict['m2'] = st.number_input("Metri quadri dell'abitazione", min_value=10)
new_input_dict['delta_pubblicazione'] = st.number_input("Da quanto tempo è in vendita la casa?", min_value=0)
new_input_dict['n posti auto'] = st.number_input("Posti auto disponibili", min_value=0)
new_input_dict['regione'] = st.selectbox('Regione',sorted(list(df['Regione'].unique()))) 
new_input_dict['citta'] = st.selectbox('Città',sorted(list(df[df['Regione']==new_input_dict['regione']]['Comune'].unique()))) 
new_input_dict['ascensore'] = st.radio('Ascensore', ['Presente', 'Assente'])
new_input_dict['ascensore'] = 1 if new_input_dict['ascensore']=='Presente' else 0
new_input_dict['box privato'] = st.radio('Box Privato', ['Presente', 'Assente'])
new_input_dict['box privato'] = True if new_input_dict['box privato']=='Presente' else False
new_input_dict['balcone'] = st.radio('Balcone', ['Presente', 'Assente'])
new_input_dict['balcone'] = True if new_input_dict['balcone']=='Presente' else False
new_input_dict['impianto tv centralizzato'] = st.radio('Impianto TV Centralizzato', ['Presente', 'Assente'])
new_input_dict['impianto tv centralizzato'] = True if new_input_dict['impianto tv centralizzato']=='Presente' else False
new_input_dict['impianto tv singolo'] = st.radio('Impianto TV Singolo', ['Presente', 'Assente'])
new_input_dict['impianto tv singolo'] = True if new_input_dict['impianto tv singolo']=='Presente' else False
new_input_dict['porta blindata'] = st.radio('Porta Blindata', ['Presente', 'Assente'])
new_input_dict['porta blindata'] = True if new_input_dict['porta blindata']=='Presente' else False
new_input_dict['arredato'] = st.radio('Completamente Arredato', ['Si', 'No'])
new_input_dict['arredato'] = True if new_input_dict['arredato']=='Si' else False
new_input_dict['parzialmente arredato'] = st.radio('Parzialmente Arredato', ['Si', 'No'])
new_input_dict['parzialmente arredato'] = True if new_input_dict['parzialmente arredato']=='Si' else False
new_input_dict['cantina'] = st.radio('Cantina', ['Presente', 'Assente'])
new_input_dict['cantina'] = True if new_input_dict['cantina']=='Presente' else False
new_input_dict['esposizione doppia'] = st.radio('Esposizione Doppia', ['Presente', 'Assente'])
new_input_dict['esposizione doppia'] = True if new_input_dict['esposizione doppia']=='Presente' else False
new_input_dict['caminetto'] = st.radio('Caminetto', ['Presente', 'Assente'])
new_input_dict['caminetto'] = True if new_input_dict['caminetto']=='Presente' else False
new_input_dict['terrazza'] = st.radio('Terrazza', ['Presente', 'Assente'])
new_input_dict['terrazza'] = True if new_input_dict['terrazza']=='Presente' else False
new_input_dict['impianto di allarme'] = st.radio('Impianto di Allarme', ['Presente', 'Assente'])
new_input_dict['impianto di allarme'] = True if new_input_dict['impianto di allarme']=='Presente' else False
new_input_dict['videocitofono'] = st.radio('Videocitofono', ['Presente', 'Assente'])
new_input_dict['videocitofono'] = True if new_input_dict['videocitofono']=='Presente' else False
new_input_dict['cancello elettrico'] = st.radio('Cancello elettrico', ['Presente', 'Assente'])
new_input_dict['cancello elettrico'] = True if new_input_dict['cancello elettrico']=='Presente' else False
new_input_dict['fibra ottica'] = st.radio('Fibra Ottica', ['Presente', 'Assente'])
new_input_dict['fibra ottica'] = True if new_input_dict['fibra ottica']=='Presente' else False
new_input_dict['armadio a muro'] = st.radio('Armadio a muro', ['Presente', 'Assente'])
new_input_dict['armadio a muro'] = True if new_input_dict['armadio a muro']=='Presente' else False
new_input_dict['mansarda'] = st.radio('Mansarda', ['Presente', 'Assente'])
new_input_dict['mansarda'] = True if new_input_dict['mansarda']=='Presente' else False
new_input_dict['portiere'] = st.radio('Portiere', ['Presente', 'Assente'])
new_input_dict['portiere'] = True if new_input_dict['portiere']=='Presente' else False
new_input_dict['piscina_idromassaggio'] = st.radio('Piscina o Idromassaggio', ['Presente', 'Assente'])
new_input_dict['piscina_idromassaggio'] = True if new_input_dict['piscina_idromassaggio']=='Presente' else False

# Convert to JSON string
input_data = json.dumps(new_input_dict)

# Make the request and display the response
if st.button('Consigliami il prezzo della proprietà'):
    # Set the content type
    headers = {"Content-Type": "application/json"}
    resp = requests.post(docker_url, input_data, headers=headers)
    price_prediction = json.loads(resp.text)
    q05 = '{:,}'.format(price_prediction['Q05'])
    q50 = '{:,}'.format(price_prediction['Q50'])
    q95 = '{:,}'.format(price_prediction['Q95'])
    st.markdown(f'''
                Per la proprietà data in input, stimo con confidenza al 90% un range di prezzo compreso tra **{q05}€** e **{q95}€**.
                
                Consiglio un prezzo di **{q50}€**''')