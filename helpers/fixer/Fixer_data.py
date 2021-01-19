import requests
from psycopg2.extras import execute_values
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

class Fixer_data():

    def __init__(self,api_key,base,symbols):
        self.api_key=api_key
        self.base=base
        self.symbols=symbols
        self.symbols_string=','.join(symbols)
        self.response=self.get_data()
        
        logging.info(self.response)


    def get_data(self):

        response = requests.get(f"http://data.fixer.io/api/latest?access_key={self.api_key}&symbols={self.symbols_string}&base={self.base}&format=1")

        return response.json()

    def get_token(client_id, client_secret,refresh=None):

        client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

        post_data = {"grant_type": 'client_credentials'}

        response = requests.post("https://data.fixer.io/oauth/token",
                                auth=client_auth,
                                data=post_data)
        token_json = response.json()

        return token_json["access_token"]


    def get_data_outh(access_token):
        headers = {"Authorization": "bearer " + access_token}
        response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
        me_json = response.json()
        return me_json['name']

    
    def insert_statement(self,cur):
        
        data_to_insert=[]
        for symbol in self.response['rates'].items():
            data_dict={}
            data_dict['currency']=symbol[0]
            data_dict['rate']=symbol[1]
            data_dict['base']=self.response['base']
            data_dict['created_at']=datetime.fromtimestamp( self.response['timestamp'])
            data_dict['inserted_at']=datetime.now()
            data_to_insert.append(data_dict)
            
        
        formatted_date=datetime.fromtimestamp( self.response['timestamp']).strftime("%Y-%m-%d")

        delete_query=f"""DELETE FROM forex_rates.fx_price_index WHERE created_at::date='{formatted_date}';"""
        
        cur.execute(delete_query)
        
        logging.info(f'Executed:{delete_query}')
        
        columns = data_to_insert[0].keys()
        query = "INSERT INTO forex_rates.fx_price_index ({}) VALUES %s".format(','.join(columns))

        # convert projects values to sequence of seqeences
        values = [[value for value in data.values()] for data in data_to_insert]

        execute_values(cur, query, values)
        
        logging.info(f'Executed:{query}')
