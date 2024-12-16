import pickle 
import pandas as pd 
from unidecode import unidecode

def fix_citta(city):
    fix_citta_dict = {'Reggio Emilia': 'REGGIO NELLEMILIA', 'Montemagno':'MONTEMAGNO MONFERRATO', 
             'Calatafimi-Segesta':'CALATAFIMI SEGESTA','Giardini-Naxos':'GIARDINI NAXOS', 'Trentola-Ducenta':'TRENTOLA DUCENTA', 
             'Bolzano':'BOLZANO/BOZEN', 'Appiano sulla Strada del Vino':'APPIANO SULLA STRADA DEL VINO/EPPAN AN DER WEINSTRASSE', 
             'Laives':'LAIVES/LEIFERS', 'Merano':'MERANO/MERAN', 'Montescudo - Montecolombo':'MONTESCUDO - MONTE COLOMBO', 
             'Crespina e Lorenzana':'CRESPINA LORENZANA'}
    
    if city in fix_citta_dict.keys():
        return fix_citta_dict[city]
    return city

def _add_population(df):
    abitanti = pd.read_csv('feature_data/abitanti.csv')
    abitanti['DESCRIZIONE COMUNE'] = abitanti['DESCRIZIONE COMUNE'].str.replace("'","").str.lower()
    abitanti.rename({'DESCRIZIONE COMUNE':'citta', 'POPOLAZIONE CENSITA TOTALE':'popolazione'}, axis=1, inplace=True)
    abitanti['popolazione']=abitanti['popolazione'].str.replace('.','').astype(int)
    df['citta'] = df['citta'].map(unidecode).str.replace("'","").map(fix_citta).str.lower()
    df = pd.merge(df, abitanti[['citta', 'popolazione']], how='left', on='citta')
    df.loc[df['popolazione'].isna(), 'popolazione']=-1
    return df

def _add_reddito(df):
    reddito = pd.read_csv('feature_data/reddito_by_regione.csv')
    reddito = reddito[reddito['T_D8']=='REDD_MEDIANO_FAM'][['Territorio', 'Value']].rename({'Territorio':'regione', 'Value':'reddito mediano'}, axis=1)
    df['regione']=df['regione'].str.lower()
    reddito['regione'] = reddito['regione'].str.lower()
    reddito.loc[reddito['regione']=="valle d'aosta / vallée d'aoste", 'regione'] = 'valle-d-aosta'
    reddito.loc[reddito['regione']=="provincia autonoma bolzano / bozen", 'regione'] = 'trentino-alto-adige'
    reddito.loc[reddito['regione']=="friuli-venezia giulia", 'regione'] = 'friuli-venezia-giulia'
    df = pd.merge(df, reddito, how='left', on='regione')
    return df

def predict_new_data(input_data):
    test_data = pd.DataFrame(input_data, index=[0])
    #Prepare Data
    test_data = _add_population(test_data)
    test_data = _add_reddito(test_data)
    #Load Encoder
    with open('artifacts/categorical_encoder.pkl', 'rb') as f:
        categorical_encoder = pickle.load(f)
    categorical_features = ['bagni','stanze','disponibilità','locali','cucina','tipologia_casa','classe_casa','tipologia_proprietà', 'giardino','infissi']
    test_data[categorical_features] = categorical_encoder.transform(test_data[categorical_features])
      
    #Load Model
    with open('artifacts/lightgbm_regressor.pkl', 'rb') as f:
        model = pickle.load(f)

    features = ['bagni','stanze','piano','m2','disponibilità','locali','delta_pubblicazione','totale_piani','ascensore','cucina',
                'camere','tipologia_casa','classe_casa','tipologia_proprietà','n posti auto','box privato','balcone','impianto tv singolo',
                'porta blindata','parzialmente arredato','cantina','esposizione doppia','arredato','caminetto','terrazza','impianto di allarme',
                'portiere','piscina_idromassaggio','videocitofono','cancello elettrico','fibra ottica','armadio a muro','impianto tv centralizzato',
                'mansarda','giardino','infissi','popolazione','reddito mediano']
    
    return round(model.predict(test_data[features])[0])