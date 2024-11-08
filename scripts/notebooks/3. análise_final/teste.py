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



cur = conn.cursor()
cur.execute('''
                SELECT concursospublicos."id"
                FROM concursospublicos;''')

data = cur.fetchall()

IDs = list([x[0] for x in data])





def nr_entidades(Id):
    """
    Função que, dado o id de um contrato, retorna uma lista com as entidades concorrentes. Desta forma, podemos calcular o número de entidades concorrentes utilizando o comando len()
    Se se der como input apenas um contrato - o id deste irá ter length = 8 visto que cada ID é composto por 8 algarismos - irá ser realizado no primeiro ramo do ciclo if-else
    Se se der um tuplo de ID's irá ser calculado no segundo ramo do ciclo e será retornada uma lista de listas

    Parâmetros:
        Id : id do contrato

    return:
        result : lista com a entidades concorrentes
    """

    
    lista_nec = list()

    if type(Id) != int : 

        cur = conn.cursor()
        cur.execute('''
                    SELECT entidades_concorrentes
                    FROM "concursospublicos"
                    WHERE id IN %s; ''', (tuple(Id),))
            
        data = cur.fetchall()
        n = len(data)
        r = [] 
        result = []
        
        for i in range(n):

            if data[i][0] == None:
                result.append(1) 

            else :
                r = data[i][0].split('|||')
                result.append(len(r)+1)  

        return result


    else :

        cur = conn.cursor()
        cur.execute('''
                    SELECT entidades_concorrentes
                    FROM "concursospublicos"
                    WHERE id = %s;''', (Id,))
        
        data = cur.fetchall()
        
        if data[0][0] == None:
            return 0

        else :
            result = data[0][0].split('|||')
            return len(result) + 1
    

# Para um contrato
id1 = IDs[0]
#print(nr_entidades(id1))

nec = (nr_entidades(IDs))

# combined_lists = list(zip(IDs, nec))

# file_name = "nec.csv"

# with open(file_name, 'w', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(['IDs', 'NEC'])  
#     csv_writer.writerows(combined_lists)



# cur = conn.cursor()
# for i,j in enumerate(nec):
#     cur.execute("UPDATE concursospublicos SET nr_entidadesconcorrentes = %s WHERE id = %s", (nec[i], IDs[i]))
#     print(i,IDs[i])
# conn.commit()
# cur.close()