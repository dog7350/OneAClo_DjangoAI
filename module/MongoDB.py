from pymongo import MongoClient


client = MongoClient(host="43.202.160.36", port=8821, username='oac', password='oac', authSource='oneaclo')
db = client['oneaclo']

inquiry = db['oacinquirylogs']
order = db['oacorderlogs']