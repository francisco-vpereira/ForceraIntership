# ---------------------------------------# 
#              Bibliotecas
# ---------------------------------------# 
import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import numpy as np
from IPython.display import HTML


# ---------------------------------------# 
#      Criar ligação com a database
# ---------------------------------------# 
conn = psycopg2.connect(
    host="localhost",
    port = 5434,
    database="aim4ps",
    user="myuser",
    password="1234")
cur = conn.cursor()


# ---------------------------------------# 
#               Funções
# ---------------------------------------# 

def preco_contrato(id_anuncio):
    '''
    Função que retorna preço contratual a partir do id do anúncio
    '''
    cur = conn.cursor()
    cur.execute('''
        SELECT preco_contratual
        FROM "CONTRACTS"
        WHERE idcontrato = %s; ''', (id_anuncio,))
    return np.asarray(cur.fetchall())[0]

#print(preco_contrato('8584389')) 



def all_ids():
    '''
    Função que retorna todos os ids dos contratos
    '''
    cur = conn.cursor()
    cur.execute(''' 
                SELECT idcontrato
                FROM "CONTRACTS";
                ''')
    return np.asarray(cur.fetchall())

ids = all_ids()
print(ids)

