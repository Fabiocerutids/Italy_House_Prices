import streamlit as st
import requests
import json
import pandas as pd

docker_url = "http://localhost:5000/predict"
df = pd.read_csv('../data/feature_data/map_comuni_regioni.csv')

st.markdown('''
    # Benvenuto al tuo assistente immobiliare!
    Tramite l'interfaccia sottostante, potrai indicarmi le informazioni di una proprietà immobiliare e ti consiglierò un range con confidenza al 90%
    sul valore di essa. Inoltre, provvederò anche a fornirti una stima puntuale sul suo valore.
    
    *Nota: Le mie previsioni non hanno un'accuratezza del 100%, considerale come indicative* 
    ''')

new_input_dict = {}
                
                
new_input_dict['bagni'] = st.pills('Bagni', ['1', '2', '3', '3+'])
new_input_dict['stanze'] = st.pills("Locali dell'abitazione", ['monolocale', 'bilocale', 'trilocale', 'quadrilocale', 'pentalocale', 'oltre pentalocale'])
new_input_dict['camere'] = st.number_input("Camere da letto", min_value=1)
new_input_dict['disponibilità'] = st.pills('Disponibilità', ['Libero', 'Futuro', 'Sconosciuta'])
new_input_dict['disponibilità'] = 'missing' if new_input_dict['disponibilità']=='Sconosciuta' else new_input_dict['disponibilità']
new_input_dict['cucina'] = st.pills('Tipologia cucina',['cucina abitabile', 'cucina semi abitabile','cucina angolo cottura', 'cucina a vista', 'no info','cucina cucinotto'])
new_input_dict['tipologia_casa'] = st.selectbox('Tipologia abitazione', ['Appartamento','Appartamento in villa','Attico','Baglio','Baita','Casa colonica','Casale','Cascina','Chalet','Dammuso','Loft','Mansarda','Open space','Palazzo - Edificio','Rustico','Sasso','Terratetto plurifamiliare','Terratetto unifamiliare','Villa a schiera','Villa bifamiliare','Villa plurifamiliare','Villa unifamiliare']) 
new_input_dict['classe_casa'] = st.pills('Classe immobiliare', ['Classe immobile economica','Classe immobile media','Classe immobile signorile','Immobile di lusso','Sconosciuta'])
new_input_dict['classe_casa'] = 'missing' if new_input_dict['classe_casa']=='Sconosciuta' else new_input_dict['classe_casa']
new_input_dict['tipologia_proprietà'] = st.pills('Tipologia di proprietà', ['Diritto di superficie','Intera proprietà','Multiproprietà','Nuda proprietà','Parziale proprietà','Sconosciuta'])
new_input_dict['tipologia_proprietà'] = 'missing' if new_input_dict['tipologia_proprietà']=='Sconosciuta' else new_input_dict['tipologia_proprietà']
new_input_dict['giardino'] = st.pills('Giardino', ['comune','privato','assente'])
new_input_dict['giardino'] = 'missing' if new_input_dict['giardino']=='assente' else new_input_dict['giardino']
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
new_input_dict['da ristrutturare'] = st.radio("L'abitazione è da ristrutturare?", ['Sì', 'No'])
new_input_dict['da ristrutturare'] = True if new_input_dict['da ristrutturare']=='Sì' else False
new_input_dict['ristrutturato'] = st.radio("L'abitazione risulta ristrutturata?", ['Sì', 'No'])
new_input_dict['ristrutturato'] = True if new_input_dict['ristrutturato']=='Sì' else False
new_input_dict['ben collegato'] = st.radio('Ben collegato', ['Sì', 'No'])
new_input_dict['ben collegato'] = True if new_input_dict['ben collegato']=='Sì' else False
new_input_dict['lavanderia'] = st.radio('Lavanderia', ['Presente', 'Assente'])
new_input_dict['lavanderia'] = True if new_input_dict['lavanderia']=='Presente' else False
new_input_dict['ripostiglio'] = st.radio('Ripostiglio', ['Presente', 'Assente'])
new_input_dict['ripostiglio'] = True if new_input_dict['ripostiglio']=='Presente' else False
new_input_dict['bagno finestrato'] = st.radio('Bagno Finestrato', ['Presente', 'Assente'])
new_input_dict['bagno finestrato'] = True if new_input_dict['bagno finestrato']=='Presente' else False
new_input_dict['luminoso'] = st.radio("L'abitazione è luminosa", ['Sì', 'No'])
new_input_dict['luminoso'] = True if new_input_dict['luminoso']=='Sì' else False
new_input_dict['parquet'] = st.radio('Parquet', ['Presente', 'Assente'])
new_input_dict['parquet'] = True if new_input_dict['parquet']=='Presente' else False
new_input_dict['aria condizionata'] = st.radio('Aria Condizionata', ['Presente', 'Assente'])
new_input_dict['aria condizionata'] = True if new_input_dict['aria condizionata']=='Presente' else False
new_input_dict['parchi e verde'] = st.radio("Sono presenti parchi e verde intorno all'abitazione?", ['Sì', 'No'])
new_input_dict['parchi e verde'] = True if new_input_dict['parchi e verde']=='Sì' else False
new_input_dict['ultimo'] = st.radio("La proprietà si trova all'ultimo piano", ['Sì', 'No'])
new_input_dict['ultimo'] = True if new_input_dict['ultimo']=='Sì' else False

# Convert to JSON string
input_data = json.dumps(new_input_dict)

# Make the request and display the response
if st.button('Consigliami il prezzo della proprietà'):
    # Set the content type
    headers = {"Content-Type": "application/json"}
    resp = requests.post(docker_url, input_data, headers=headers)
    price_prediction = json.loads(resp.text)
    q05 = '{:,}'.format(round(price_prediction['Q05']/1000)*1000)
    q50 = '{:,}'.format(round(price_prediction['Q50']/1000)*1000)
    q95 = '{:,}'.format(round(price_prediction['Q95']/1000)*1000)
    st.markdown(f'''
                Per la proprietà data in input, stimo con confidenza al 90% un range di prezzo compreso tra **{q05}€** e **{q95}€**.
                
                Consiglio un prezzo di **{q50}€**''')