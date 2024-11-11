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

from functions import *




# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# LIGAR À BASE DE DADOS
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
conn = psycopg2.connect(
    host = "contratos-base-gov1.cf87yxnqgph8.eu-central-1.rds.amazonaws.com",
    port = 5432,
    #database = "contratosbasegov",
    user = "contratosbasegov",
    password = "")

cur = conn.cursor()





# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# FUNÇÕES PARA CADA FLAG 
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

def redflag(pbase, pcontr, tol, ids, r, df):
    
    """
    Função que calcula a diferença entre o preço base e preço contratual de um contrato realizado
    Se o preço contratual estiver contido num intervalo em torno do preço base é levantada um flag
    O intervalo é definido pelo parâmetro tolerância e é definido como : [preço_base - preço_base*tolerância, preço_base + preço_base*tolerância]
    Se o preço base não estiver definido, é levantada uma flag também 

    Parâmetros de entrada : 
        pbase : array com os preços base
        pcontr : array com os preços contratuas
        tol : valor da tolerância. Só pode tomar valores entre 0 e 1
        ids : id's dos contratos em questão
        r : ratio máximo permitido entre preço base / preço contratual
        df : dataframe que contém todos os contratos públicos. Necessitamos deste parâmetro para usar na função racio( )

    Return : 
        f : tuplo com os id's dos contratos com flag associada
    """

    # Garantir que dimensão dos arrays com os preços é igual
    if len(pbase) != len(pcontr):
        return "Error : dim pbase != dim pcontr"

    # Garantir que tolerância é um numero entre 0 e 1
    if tol < 0 or tol > 1 :
        return "Error : tolerance must belong between 0 and 1"

    # Número de preços base
    n = len(pbase)

    # Array que guarda ocorrência - ou não - de uma flag
    flags = np.zeros(n)
    
    # Disparar flag se preço contratual for superior ao preço base
    flags[np.where(pcontr > pbase)[0]] = 1
    
    # Disparar flag se preço contratual for nulo ( campo não preenchido no basegov / potencial má prática )
    flags[np.where(pcontr == 0)[0]] = 1

    # Disparar flag se preço base for nulo ( campo não preenchido no basegov / potencial má prática )
    flags[np.where(pbase == 0)[0]] = 1

    # Se o preço contratual for superior ao preço base OU estiver muito perto, no limite inferior, do preço base é ativada a flag
    # Para isso, vamos definir um valor limite inferior - lo_lim - a partir do qual é ativada a flag 
    lo_lim = pbase * (1-tol)
    flags[np.where(pcontr > lo_lim)[0]] = 1


    # Para todos os contratos em que se verifique que o rácio precobase/precocontratual é superior a um dado valor
    # é preciso verificar se existem outros lotes. Para isso, identificamos o nr de anuncio
    flags1 = np.where(pbase/pcontr > r)[0]
    coiso = racio(flags1, df, r = 5)

    if len(coiso) > 0:
        flags[coiso[0]] = 1


    # Conversão do tuplo de ids num array de uma coluna
    # Assim conseguimos ver quais são os contratos com flag = 1
    ids = np.array(ids).reshape((n,))

    # Contratos com ocorrência de uma flag ( posições / índices ) 
    pos = np.where(flags != 0)[0]
    
    # Selecionar contratos onde ocorre flag
    f = ids[pos]

    # Conversão do conjunto de contratos em tuplo para poder usar como input nas funções que têm como input id's de contratos
    f = f.reshape((len(f),1))
    f = tuple(map(tuple,f))
    return f





def redflag2(t,ids):
    
    """
    Função que verifica, dentro dos ajustes diretos, se o preço contratual é superior a 20.000€
    Só funciona para Aquisição de Serviços

    Parâmetros : 
        t : dataframe com todos os ajustes diretos. Esta dataframe é o  output da função 'contratos'
        ids : id's dos contratos que dizem respeito aos ajustes diretos. Estes id's são dados pelo output da função CPV

    Return :
        tuplo : f é o conjunto de contratos onde é disparada uma flag
    """

    n = len(t)

    c = t.TipoProcedimento.unique()
    #print(c)
    
    flags = np.zeros(n)
    
    #for i in range(n):
    #    if t.TipoProcedimento[i] == 'Aquisição de serviços':
    #        if t.PrecoContratual[i] > 20000:
    #            flags[i] = 1

    prices = t.PrecoContratual
    flags[np.where(prices > 20000)] = 1

    fundamento = t.iloc[:,21]
    flags[np.where(fundamento == "")] = 1
    
    # Conversão do tuplo de ids num array de uma coluna
    ids = np.array(ids).reshape((n,))

    # Contratos com ocorrência de uma flag
    pos = np.where(flags != 0)

    # Selecionar contratos onde ocorre flag
    f = ids[pos]

    # Conversão do conjunto de contratos em tuplo para poder usar como input nas funções que têm como input id's de contratos
    f = f.reshape((len(f),1))
    f = tuple(map(tuple,f))

    return f


def prazo(df):
    """
    Função que dispara flag em contratos públicos com prazo de candidatura inferior a 6 dias
    
    Parâmetros:
        df : dataframe que contém os contratos públicos
    
    return:
        flag : tuplo de id's 
    """
    
    df = df.rename(columns={0:'ID', 1:'NrAnuncio', 2:'PrecoBase', 3:'Prazo', 16:'DataPub', 17:'DataCel', 18:'PrecoContratual'})
    ID = df.ID
    
    # Índices onde não foi preenchido data de prazo de candidatura
    null_date = np.where(df.Prazo == '')[0]

    # Converter datas não preenchidas em zero
    df.loc[df['Prazo'] == '', 'Prazo'] = '0'

    # Converter dias em float para poder detetar valores inferiores a 6 dias
    df.Prazo = df.Prazo.astype(float)

    # Índices de contratos - suspeitos - com prazo inferior a 6 dias
    sus = np.where(df.Prazo < 6)[0]

    # Selecionar contratos onde ocorre flag
    flag = ID[sus]

    # Conversão do conjunto de contratos em tuplo para poder usar como input nas funções que têm como input id's de contratos
    flag = tuple(flag)
    
    return flag 


