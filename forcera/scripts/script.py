import os
os.chdir("/home/francisco/MECAD/COMP/comp")



import psycopg2
from psycopg2 import OperationalError

conn = psycopg2.connect(
    host="localhost",
    port = 5434,
    database="aim4ps",
    user="myuser",
    password="1234")



cur = conn.cursor()  
# execute a statement"public".
#cur.execute('SELECT * from "public"."CONTRACTS" LIMIT 10;')

# display the PostgreSQL database server version
#db_version = cur.fetchone()
#print(db_version)


cur.execute('''
    SELECT COUNT(*) FROM "public"."CONTRACTS";
''')

print("Número de contratos : ", cur.fetchone())

cur = conn.cursor()
cur.execute('''
    SELECT tipo_procedimento, COUNT (tipo_procedimento)
    FROM "CONTRACTS"
    GROUP BY "tipo_procedimento";
''')

(cur.fetchall())
