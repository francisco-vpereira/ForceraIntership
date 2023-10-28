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
    cur = conn.cursor()
    cur.execute('''
        SELECT preco_contratual
        FROM "CONTRACTS"
        WHERE idcontrato = %s; ''', (id_anuncio,))
    return np.asarray(cur.fetchall())[0]


# ------------------------------------------------------------------------------- # 


def preco_contrato1(ide, table):
    '''
    Função que retorna preço contratual a partir do id do anúncio para um data tabela

    Parâmetros :
        - ide : id do anúncio
        - table : tabela de interesse

    Return : 
        - int : preço contratual
    '''
    cur = conn.cursor()
    cur.execute('''
        SELECT preco_contratual
        FROM "{}"
        WHERE idcontrato = %s; '''.format(table), (ide,))
    return np.asarray(cur.fetchone())[0]


# ------------------------------------------------------------------------------- # 


def all_ids(table):
    '''
    Função que retorna todos os ids dos contratos de uma tabela

    Parâmetros :    
        - table : tabela de interesse

    Return : 
        - numpy array : ids de todos os contratos de uma tabela 
    '''

    cur = conn.cursor()
    cur.execute(''' 
                SELECT idcontrato
                FROM "{}"; '''.format(table)) 
    return np.asarray(cur.fetchall())


# ------------------------------------------------------------------------------- # 


def col_names(table):
    '''
    Função que retorna os nomes das colunas de uma tabela
    
    Parâmetros : 
        - table : tabela de interesse

    return : 
        - pandas DataFrame : nomes das colunas
    '''

    cur = conn.cursor()
    cur.execute('''
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s;''', (table,))

    cnames = pd.DataFrame(cur.fetchall())
    # cnames = [row[0] for row in cur.fetchall()]
    return cnames


# ------------------------------------------------------------------------------- # 


def n_contracts(table):
    '''
    Retorna o número de contratos de uma tabela pertencente à base de dados

    Parâmetros : 
        - table : tabela de interesse

    return : 
        - int : número de contrato
    '''
    
    cur = conn.cursor()
    cur.execute('''
                SELECT COUNT(*) 
                FROM "{}"; '''.format(table))
    ncontract = cur.fetchone()[0]
    return ncontract

