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


# Obter valoes das colunas pertecentes à tabela "concursos_publicos" de concursos publicos referentes ao dia de ontem
cur = conn.cursor()
cur.execute('''
    SELECT
        contratos_basegov."id",
        contratos_basegov."data_publicacao",
        contratos_basegov."contractTypes",
        contratos_basegov.fundamentacao,
        contratos_basegov.entidade_adjudicante,
        contratos_basegov.entidades_contratadas,
        contratos_basegov.entidades_concorrentes,
        contratos_basegov."executionPlace"
    FROM contratos_basegov
    WHERE data_publicacao = %s AND tipo_procedimento = 'Concurso público';
''', (ontem,))

ids_ontem = cur.fetchall()


# Inserir os valores extraidos na query anterior na tabela "concursos_publicos"
cur = conn.cursor()
for i in ids_ontem:
    cur.execute('''
        INSERT INTO concursos_publicos(
            id,
            data_publicacao,
            "contractTypes",
            fundamentacao,
            entidade_adjudicante,
            entidades_contratadas,
            entidades_concorrentes,
            "executionPlace"
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    ''', i)

conn.commit()


# Dar update às colunas auxiliares da tabela concursos_publicos
cur = conn.cursor()
cur.execute('''
            UPDATE concursos_publicos
            SET 
                adjudicante = split_part(split_part(entidade_adjudicante, '(', 1), ')', 1),
                nif1 = split_part(split_part(entidade_adjudicante, '(', 2), ')', 1),
                url1 = split_part(entidade_adjudicante, ')(', 2),
                adjudicataria = split_part(split_part(entidades_contratadas, '(', 1), ')', 1),
                nif2 = split_part(split_part(entidades_contratadas, '(', 2), ')', 1),
                url2 = split_part(entidades_contratadas, ')(', 2),
                nr_entidadesconcorrentes = CARDINALITY(STRING_TO_ARRAY(entidades_concorrentes, '|||')) + 1
            WHERE data_publicacao = %s;
            ''', (ontem,))
conn.commit()



cur = conn.cursor()
cur.execute('''
            UPDATE concursos_publicos
            SET nr_entidadesconcorrentes = COALESCE(nr_entidadesconcorrentes, 1)
            WHERE data_publicacao = %s;
            ''', (ontem,))
conn.commit()






cur = conn.cursor()
cur.execute('''
            SELECT id, concursos_publicos."contractTypes"
            FROM concursos_publicos
            WHERE data_publicacao = %s;
            ''', (ontem,))

tcs = cur.fetchall()



cur = conn.cursor()
for i in tcs:

    if 'obras' in i[1]:
        cur.execute('''
                    UPDATE concursos_publicos
                        SET tipo_contrato = 'Empreitadas'
                    WHERE id = %s;
                    ''', (i[0],))
        conn.commit()

    else:
        cur.execute('''
            UPDATE concursos_publicos
                SET tipo_contrato = 'Bens e Serviços'
            WHERE id = %s;
            ''', (i[0],))
        conn.commit()
        
        





cur = conn.cursor()
cur.execute('''
    SELECT contratos_basegov."id"
    FROM contratos_basegov
    WHERE data_publicacao = %s AND tipo_procedimento = 'Concurso público';
''', (ontem,))

idsontem = cur.fetchall()


# Escrever valores dos IDs de ontem na tabela
# Inicialmente, definir o valor das flags binárias como false. Serão atualizadas nos passos seguintes
cur = conn.cursor()
for i in idsontem:
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
                WHERE contratos_basegov."data_publicacao" = %s AND 
                    (concursos_publicos."tipo_contrato" = 'Empreitadas' AND contratos_basegov."anuncio_proposalDeadline" < 14) 
                    OR
                    (concursos_publicos."tipo_contrato" = 'Bens e Serviços' AND contratos_basegov."anuncio_proposalDeadline" < 6)
                );
            ''', (ontem,))
conn.commit() 




# # Obter IDs de ontem referentes à flag R018 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "R018" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id"
                FROM contratos_basegov
                JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                WHERE contratos_basegov."data_publicacao" = %s AND concursos_publicos."nr_entidadesconcorrentes" = 1
	        );''', (ontem,))
conn.commit() 





# # Obter IDs de ontem referentes à flag RF2 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "RF2" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id" 
                FROM contratos_basegov
                WHERE contratos_basegov."data_publicacao" = %s AND tipo_procedimento = 'Concurso público' 
                    AND TO_CHAR(contratos_basegov."anuncio_drPublicationDate", 'MM-DD') 
                    IN ('01-01', '04-25', '05-01', '06-10', '08-15','10-05', '11-01', '12-01', '12-08', '12-25')
                );''', (ontem,))
conn.commit() 





# # Obter IDs de ontem referentes à flag RF3 e dar update na tabela
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "RF3" = true
            WHERE table_temp."id" IN (
            SELECT contratos_basegov."id" 
                FROM contratos_basegov 
                WHERE contratos_basegov."data_publicacao" = %s AND contratos_basegov."totalEffectivePrice" > 0 AND ABS(contratos_basegov."totalEffectivePrice" - preco_contratual) > 0
                );
            ''', (ontem,))
conn.commit() 