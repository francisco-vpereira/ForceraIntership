# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# BIBLIOTECAS 
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from IPython.display import HTML
import webbrowser





# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# LIGAR À BASE DE DADOS
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
conn = psycopg2.connect(
    host = "contratos-base-gov1.cf87yxnqgph8.eu-central-1.rds.amazonaws.com",
    port = 5432,
    #database = "contratosbasegov",
    user = "contratosbasegov",
    password = "8n9nyeTBFUyCcLJShNrZdPUai2KQkue4")

cur = conn.cursor()





# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# FUNÇÕES PARA EXPLORAR O CONJUNTO DE DADOS
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #


def h(df):
    """
    Função que permite ver dataframe completa e de forma mais organizada
    """
    return HTML(df.to_html(index=False))




def url(id):
    """
    Função que abre página web do anúncio a partir do id do contrato. Só funciona para um contrato de cada vez
    """
    
    cur = conn.cursor()

    cur.execute('''
        SELECT "url_anuncio"
        FROM "contratos"
        WHERE "id" = %s;''',(id, ))

    return webbrowser.open(cur.fetchall()[0][0])    





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
    #cnames = [row[0] for row in cur.fetchall()]
    return cnames





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

#print(n_contracts("contratos"))





def all_ids(table):
    '''
    Função que retorna todos os ids dos contratos de uma tabela

    Parâmetros :    
        - table : tabela de interesse

    Return : 
        - list : ids de todos os contratos de uma tabela 
    '''

    cur = conn.cursor()
    cur.execute(''' 
                SELECT id
                FROM "{}"; '''.format(table)) 
    return list(cur.fetchall())





def ajuste_dir():
    """
    Função que retorna os ID's de todos os ajustes diretos em regime geral celebrados
    """
    
    cur = conn.cursor()
    
    cur.execute('''
            SELECT "id"
            FROM "contratos"
            WHERE tipo_procedimento = 'Ajuste Direto Regime Geral';''')
    
    return list(cur.fetchall())





def consulta_prev():
    """
    Função que retorna os ID's de todas as consultas prévias celebradas
    """
    
    cur = conn.cursor()
    
    cur.execute('''
            SELECT "id"
            FROM "contratos"
            WHERE tipo_procedimento = 'Consulta Prévia';''')
    
    return list(cur.fetchall())





def concurso_pub():
    """
    Função que retorna os ID's de todos os concursos públicos celebrados
    """
    
    cur = conn.cursor()
    
    cur.execute('''
            SELECT "id"
            FROM "contratos"
            WHERE tipo_procedimento = 'Concurso público';''')
    
    return list(cur.fetchall())





def cpv_direto(cpv):
    
    """
    Função que retorna os id's de todos os contratos para um determinado CPV para todos os Ajustes Diretos em Regime Geral

    Parâmetros :
        cpv : inserir os dois algarismos iniciais do CPV entre '' ( https://www.publictendering.com/cpv-codes/list-of-the-cpv-codes/ )
    
    Return :
        tuple : id's dos contratos
    """
    
    cur = conn.cursor()
    cur.execute('''
                SELECT "id"
                FROM "contratos"
                WHERE cpv LIKE %s AND tipo_procedimento = 'Ajuste Direto Regime Geral';''', (cpv + '%',))
    
    return cur.fetchall()





def cpv_cpub(cpv):

    """
    Função que retorna os id's de todos os contratos para um determinado CPV para todos os Concursos Públicos

    Parâmetros :
        cpv : inserir os dois algarismos iniciais do CPV entre '' ( https://www.publictendering.com/cpv-codes/list-of-the-cpv-codes/ )
    
    Return :
        tuple : id's dos contratos
    """
    
    cur = conn.cursor()
    cur.execute('''
                SELECT "id"
                FROM "contratos"
                WHERE cpv LIKE %s AND tipo_procedimento = 'Concurso público';''', (cpv + '%',))

    
    return cur.fetchall()





def cpv(cpv, proc):

    """
    Função que retorna os id's de todos os contratos para um determinado CPV para todos os Concursos Públicos

    Parâmetros :
        cpv : inserir os dois algarismos iniciais do CPV entre '' ( https://www.publictendering.com/cpv-codes/list-of-the-cpv-codes/ )
    
    Return :
        tuple : id's dos contratos
    """
    
    cur = conn.cursor()
    cur.execute('''
                SELECT "id"
                FROM "contratos"
                WHERE cpv LIKE %s AND tipo_procedimento = %s;''', (cpv + '%', proc))

    
    return cur.fetchall()





def contrato(ide):
    '''
    Função que retorna linha da database referente ao contrato com id = ide
    '''
        
    cur = conn.cursor()
    cur.execute('''
        SELECT *
        FROM "contratos"
        WHERE id = %s; ''', (ide,))
    return pd.DataFrame(cur.fetchall())





def contratos(ide):
    '''
    Função que retorna contratos referentes a um conjunto de ids

    Parâmetros :
        ide : tuplo de id's de anúncios

    return:
        dataframe com contratos
    '''
        
    cur = conn.cursor()
    cur.execute('''
        SELECT *
        FROM "contratos"
        WHERE id IN %s; ''', (tuple(ide),))
    return pd.DataFrame(cur.fetchall())





def preco_contrato1(ide):
    '''
    Função que retorna preço contratual a partir do id do anúncio para a tabela "contratos"

    Parâmetros :
        - ide : id do anúncio

    Return : 
        - int : preço contratual
    '''
        
    cur = conn.cursor()
    cur.execute('''
        SELECT preco_contratual
        FROM "contratos"
        WHERE id = %s; ''', (ide,))
    return float(cur.fetchone()[0])





def preco_contrato2(ide, table = ""):
    '''
    Função que retorna preço contratual a partir do id do anúncio para um dada tabela

    Parâmetros :
        - ide : id do anúncio
        - table : tabela de interesse. Caso input esteja vazio, usar tabela 'contratos'

    Return : 
        - int : preço contratual
    '''

    if table == "": 
        table = "contratos"
        
    cur = conn.cursor()
    cur.execute('''
        SELECT preco_contratual
        FROM "{}"
        WHERE id = %s; '''.format(table), (ide,))
    return float((cur.fetchone())[0])





#def preco_contrato3(id_anuncio):
#    
#    '''
#    Função que retorna preço contratual a partir de uma lista de ids de anúncios
#    '''
#    
#    cur.execute('''
#        SELECT preco_contratual
#        FROM "contratos"
#        WHERE id IN %s; ''', (tuple(id_anuncio),))
#    
#    return np.array(cur.fetchall()[0])





def preco_contrato3(id_anuncio):
    
    '''
    Função que retorna preço contratual a partir de uma lista de ids de anúncios
    '''
    
    cur.execute('''
        SELECT preco_contratual
        FROM "contratos"
        WHERE id IN %s; ''', (tuple(id_anuncio),))

   #preco = list(cur.fetchall())
   #
   #n = len(preco)
   #p = np.zeros(n)

   #for i in range(n):
   #    p[i] = (preco[i][0]).replace(".", "").replace(",",".").replace("€","")

    p = np.array(cur.fetchall(), dtype = float).reshape(len(id_anuncio),)
    return p





def preco_contrato4(ide, table = ""):
    '''
    Função que retorna preço contratual a partir de uma lista de ids de anúncios para uma determinada tabela

    Parâmetros :
        - ide : id do anúncio
        - table : tabela de interesse. Caso input esteja vazio, usar tabela 'contratos'

    Return : 
        - int : preço contratual
    '''

    
    if table == "": 
        table = "contratos"

    
    cur.execute('''
        SELECT preco_contratual
        FROM "{}"
        WHERE id IN %s; '''.format(table), (tuple(ide),))
    
    return np.asarray(cur.fetchall())
    




def preco_base(ide):
    '''
    Função que retorna preço base a partir do id do anúncio para a tabela "contratos"

    Parâmetros :
        - ide : id do anúncio

    Return : 
        - tuplo : preço contratual
    '''
        
    cur = conn.cursor()
    cur.execute('''
        SELECT anuncio_preco_base
        FROM "contratos"
        WHERE id = %s; ''', (ide,))
    
    return cur.fetchone()





def preco_base1(ide):
    '''
    Função que retorna preço base a partir do id do anúncio para a tabela "contratos"

    Parâmetros :
        - ide : id do anúncio

    Return : 
        - int : preço contratual
    '''
        
    cur = conn.cursor()
    cur.execute('''
        SELECT anuncio_preco_base
        FROM "contratos"
        WHERE id = %s; ''', (ide,))


    preco = cur.fetchone()[0]
    p1 = float(preco[:-2].replace(".", "").replace(",","."))
    
    return p1





def preco_base2(ide, table = ""):
    '''
    Função que retorna preço base a partir do id do anúncio para um dada tabela

    Parâmetros :
        - ide : id do anúncio
        - table : tabela de interesse. Caso input esteja vazio, usar tabela 'contratos'

    Return : 
        - int : preço contratual
    '''

    if table == "": 
        table = "contratos"


    cur = conn.cursor()
    cur.execute('''
        SELECT anuncio_preco_base
        FROM "{}"
        WHERE id = %s; '''.format(table), (ide,))


    preco = cur.fetchone()[0]

    if preco != 0:
        p1 = float(preco[:-2].replace(".", "").replace(",","."))
    else:
        p1 = 0
    
    return p1





def preco_base3(id_anuncio):
    
    '''
    Função que retorna preço base a partir de uma lista de ids de anúncios
    '''
    
    cur.execute('''
        SELECT anuncio_preco_base
        FROM "contratos"
        WHERE id IN %s; ''', (tuple(id_anuncio),))
    
    preco = list(cur.fetchall())
    #return preco    
    
    # Como os valores do preco base estão no formato ---.---,--€ é precio converter em -------.-- para comparar posteriormente
    n = len(preco)
    p = np.zeros(n)
    
    for i in range(n):
    
       if preco[i][0] != 'None':
           #p[i] = (preco[i][0]).replace(".00", "").replace(".", "").replace(",",".").replace("€","")
           p[i] = (preco[i][0])
    
       else:
           pass
           
    return p


# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# TRATAMENTO DOS LOTES 
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

def racio(indice, df, r):
    
    """
    Função que, para um determinado ID de contrato, verifica se existem outros ID's com o mesmo número de anúncio
    Se existirem, soma todos os de preços contratuais e compara ao preço base
    Esta função só se aplica para valores do rácio pb/pc superiores a um determinado valor e irá apenas ser chamada dentro da função
    redflags2

    Parâmetros:
        indice : índices dos anúncios com racio superior a limite
        df : dataframe que contém todos os contratos públicos
        r : racio máximo tolerado
    """

    if len(indice) == 0:
            return 0 
        
    # Número de anúncio para os contratos acima de um certo rácio
    n_anuncio = df.iloc[indice,1]

    df = df.rename(columns={2:'PrecoBase', 18:'PrecoContratual'})
    df.PrecoContratual = df.PrecoContratual.replace('None', 0).astype(float)
    df.PrecoBase = df.PrecoBase.replace('None', 0).astype(float)
    
    # Create a pandas Series from the column values
    serie = pd.Series(n_anuncio)
    
    # Get counts of each unique value and their indices
    value_counts = serie.value_counts().reset_index()
    value_counts.columns = ['NumberID', 'NrOccurrence']
    
    # Get indices of each unique value
    indices = serie.reset_index()
    indices.columns = ['Lotes', 'NumberID']
    indices = indices.groupby('NumberID')['Lotes'].apply(list).reset_index()
    
    # Merge the counts and indices into a single dataframe
    result_df = pd.merge(value_counts, indices, on='NumberID')

    n = len(result_df)
    pbase = np.zeros(n)
    pcont = np.zeros(n)
    div   = np.zeros(n)
    
    for i in range(n):
        pbase[i] = np.mean(df.PrecoBase.iloc[result_df.Lotes[i]])
        pcont[i] = np.sum(df.PrecoContratual.iloc[result_df.Lotes[i]])
        div[i] = pbase[i]/pcont[i]

    pbase = pd.Series(pbase)
    pcont = pd.Series(pcont)
    div = pd.Series(div)
    
    result_df['PrecoBase'] = pbase
    result_df['PrecoContratualSoma'] = pcont
    result_df['Rácio'] = div

    # print(result_df) se quisermos ver a dataframe completa 

    # Índices onde rácio continua a ser maior do que a tolerância
    A = (np.where(result_df.Rácio > r))[0]

    # Índices dos lotes 
    B = np.array(result_df.Lotes[A])


    if len(indice) == 1:
        return B

    else:
        # Converter solução num array 1D
        flat_array = np.concatenate([np.array(sublist) for sublist in B])
        return flat_array


# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# ATRIBUIR VALOR CONTÍNUO À FLAG QUE COMPARA PREÇO BASE COM PREÇO CONTRATUAL
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

def exp1(x):
    """
    Ramo da função para x pertencente [0,10]
    """
    a = 1 ; b = 2
    return a * np.exp(-b * x)

def poly(x):
    """
    Ramo da função para x pertencente [50,inf[
    """

    a = 1.08571429e-04  
    b = 3.71428571e-03 
    c = -4.57142857e-01
    
    return a*x**2 + b*x + c

def difrel(a,b):
    """
    Calcula diferença relativa entre preço base e preço contratual
    """
    return abs(a-b)/a * 100


def fun(x):
    """
    Atribui um valor de 0 a 1 consoante o valor da diferença entre preço base e preço contratual
    """ 
    
    n = len(x)
    score = np.zeros(n)

    for i in range(n):
        
        if x[i] < 10 :
            score[i] = exp1(x[i])

        elif x[i] > 10 and x[i] < 50:
            score[i] = 0

        elif 50 <= x[i] <= 100:
            score[i] = poly(x[i])

        else:
            score[i] = 1

    return score

def flagconti(fl):
    """
    Função flag contínua : determina preço base e preço contratual a partir dos id's dos contratos. Neste caso, são os id's correspondentes às flags ativadas. 
    Calcula o valor da diferença relativa usando a função anteriormente definida : difrel()
    Por fim, para cada valor da diferença, atribui um valor entre 0 e 1
    """
    Pb = preco_base3(fl)
    Pc = preco_contrato3(fl)
    percentage = difrel(Pb,Pc)
    return Pb, Pc, percentage , fun(percentage)