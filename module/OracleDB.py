import oracledb

oracledb.init_oracle_client()
con = oracledb.connect(user="fintech", password="fintech", dsn="43.202.160.36:8819", service_name="oneaclo")

cursor = con.cursor()