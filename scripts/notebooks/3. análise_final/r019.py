import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import curve_fit
import seaborn as sns
from IPython.display import HTML
import webbrowser
from collections import defaultdict
import networkx as nx
import csv
import os
os.chdir('/home/francisco/MECAD/2º Ano/Estágio/forcera/scripts/scripts_py')



# LIGAÇÃO À BASE DE DADOS
conn = psycopg2.connect(
    host = "contratos-base-gov1.cf87yxnqgph8.eu-central-1.rds.amazonaws.com",
    port = 5432,
    #database = "contratosbasegov",
    user = "contratosbasegov",
    password = "8n9nyeTBFUyCcLJShNrZdPUai2KQkue4")
cur = conn.cursor()


# Dataframe com CPV(2 digitos), ID e NR_entidadesconcorrentes
cur = conn.cursor()
cur.execute('''
                SELECT cpv2, concursospublicos."id", nr_entidadesconcorrentes
                FROM concursospublicos
                ORDER BY cpv2 DESC;''')

data = pd.DataFrame(cur.fetchall())

CPV = (data.iloc[:,0].unique())


m = np.zeros([len(CPV),10])
m[:,0] = CPV

for i,j in enumerate(CPV):
    
    res = data.loc[data.iloc[:,0] == j ,data.columns[2]]
    m[i,1] = res.values.sum()
    m[i,2:] = list(res.describe())


table_name = 'cpv_stat'
column_names = ['cpv', 'nec_t', 'count', 'mean', 'std', 'min', 'q1', 'q2', 'q3', 'max']


# Correr apenas uma vez. Caso contrário, adiciona linhas com a mesma info

for row in m:
    insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(
        sql.Identifier(table_name),
        sql.SQL(',').join(sql.Identifier(name) for name in column_names),
        sql.SQL(',').join(sql.Literal(value) for value in row)
    )
    cur.execute(insert_query)

conn.commit()