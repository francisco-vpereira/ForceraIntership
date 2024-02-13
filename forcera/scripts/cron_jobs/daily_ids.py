import psycopg2
from psycopg2 import OperationalError
from psycopg2 import sql
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
from datetime import datetime, timedelta




# LIGAÇÃO À BASE DE DADOS
conn = psycopg2.connect(
    host = "contratos-base-gov1.cf87yxnqgph8.eu-central-1.rds.amazonaws.com",
    port = 5432,
    #database = "contratosbasegov",
    user = "contratosbasegov",
    password = "8n9nyeTBFUyCcLJShNrZdPUai2KQkue4")




# Definir dia
yesterday = datetime.now() - timedelta(1)
ontem = datetime.strftime(yesterday, '%Y-%m-%d')



# Obter IDs de concursos publicos de ontem
cur = conn.cursor()
cur.execute('''
            SELECT id
            FROM contratos_basegov
            WHERE data_publicacao = %s AND tipo_procedimento = 'Concurso público'
            ;''', (ontem,))
ids_ontem = cur.fetchall()




# Escrever valores na tabela
cur = conn.cursor()
for i in ids_ontem:
    cur.execute('''INSERT INTO table_temp(id, data) VALUES (%s, %s);''', (i,ontem)) 

conn.commit() 