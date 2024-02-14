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




# Definir dia de ontem no formato YYYY-MM-DD
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



# Escrever valores dos IDs de ontem na tabela
# Inicialmente, definir o valor das flags binárias como false. Serão atualizadas nos passos seguintes
cur = conn.cursor()
for i in ids_ontem:
    cur.execute('''INSERT INTO table_temp(id, data_publicacao, "R003", "R018", "RF2", "RF3") VALUES (%s, %s, false, false, false, false);''', (i,ontem)) 
conn.commit() 




# Obter IDs de ontem referentes à flag R003 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "R003" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id" 
                FROM contratos_basegov
                JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                WHERE data_publicacao = %s AND 
                    (concursos_publicos."tipo_contrato" = 'Empreitadas' AND contratos_basegov."anuncio_proposalDeadline" < 14) 
                    OR
                    (concursos_publicos."tipo_contrato" = 'Bens e Serviços' AND contratos_basegov."anuncio_proposalDeadline" < 6)
                );
            ''', (ontem,))
conn.commit() 




# Obter IDs de ontem referentes à flag R018 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "R018" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id"
                FROM contratos_basegov
                JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                WHERE data_publicacao = %s AND concursos_publicos."nr_entidadesconcorrentes" = 1
	        );''', (ontem,))
conn.commit() 





# Obter IDs de ontem referentes à flag RF2 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "RF2" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id" 
                FROM contratos_basegov
                WHERE data_publicacao = %s AND tipo_procedimento = 'Concurso público' 
                    AND TO_CHAR(contratos_basegov."anuncio_drPublicationDate", 'MM-DD') 
                    IN ('01-01', '04-25', '05-01', '06-10', '08-15','10-05', '11-01', '12-01', '12-08', '12-25')
                );''', (ontem,))
conn.commit() 





# Obter IDs de ontem referentes à flag RF3 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "RF3" = true
            WHERE table_temp."id" IN (
            SELECT contratos_basegov."id" 
                FROM contratos_basegov 
                WHERE data_publicacao = %s AND contratos_basegov."totalEffectivePrice" > 0 AND ABS(contratos_basegov."totalEffectivePrice" - preco_contratual) > 0
                );
            ''', (ontem,))
conn.commit() 















