import requests
import pandas as pd
import base64
from requests_oauthlib import OAuth2Session

id='9k1GQrfrK2BuwPWlLC6XyDrbvsUa'
secret='n11vklOFPeyTIJfjqKH8HkgJDZoa'
start = '2021-01-01T00:00:00'
end='2021-01-10T00:00:00'
step = 'day'

class cycles:
    
    def get_token(self,id,secret):
        n = str((base64.standard_b64encode(str(id+":"+secret).encode('ascii'))), 'utf-8')
        url='https://apieco.eco-counter-tools.com/token'
        headers = {
            'Authorization':'Basic '+ n,
            'Content-Type':'application/x-www-form-urlencoded',
        }
        data ='grant_type=client_credentials'
        access_token=requests.post(url, headers=headers,data=data)
        self.token = access_token.json()['access_token']
    
    def get_site_list(self):
        headers = {
            'Accept':'application/json',
            'Authorization':'Bearer '+str(self.token)
        }
        url='https://apieco.eco-counter-tools.com/api/1.0/site'  
        rep=requests.get(url,headers=headers)
        return rep.json()
    
    def get_data(self,id,start,end,step):
        print(self.token)
        headers = {
            'Accept':'application/json',
            'Authorization':'Bearer '+str(self.token)
        }
        url=f'https://apieco.eco-counter-tools.com/api/1.0/data/site/{str(id)}?begin={start}&end={end}&step={step}'
        print(url)
        rep=requests.get(url,headers=headers)
        return rep

#     def get_processed_data(self,id,begin=dates().weekago,end=dates().today,step='day'):
#         raw=self.get_data(id,begin,end,step)
#         try:
#             x=[int(n['counts']) for n in raw]
#             y=[datetime.datetime.strptime(n['date'][:-5],"%Y-%m-%dT%H:%M:%S") for n in raw]
#             z=sum(x)
#         except:
#             return {'date':[],'count':[],'total':0}
#         return {'date':y,'count':x,'total':z}

data = cycles()
c = data.get_token(id,secret)
d = data.get_site_list()
e=data.get_data(id,start,end,step)
print(e)
