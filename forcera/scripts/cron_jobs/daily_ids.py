# Packages
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import sql

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from datetime import datetime, timedelta

import os
from dotenv import load_dotenv
dotenv_path = os.path.expanduser('~/.pwds.env')
load_dotenv(dotenv_path)



# Conexão à base de dados
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


conn = psycopg2.connect(
                host = db_host,
                port = db_port,
                user = db_user,
                password = db_password
        )



# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ UPDATE DA TABELA AUXILIAR ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


# Obter o último ID copiado para a tabela concursos_publicos
cur = conn.cursor()
cur.execute('''
            SELECT
                concursos_publicos."id"
            FROM concursos_publicos
            ORDER BY data_publicacao DESC, concursos_publicos."id" DESC
            LIMIT 1;
            ''')
last_id = cur.fetchone()[0]



# Copiar dados dos novos contratos adicionados à tabela contratos_basegov 
# Dados são copiados desde o contrato com o ID mais recente até ao contrato com o 
# ID mais recente da tabela auxiliar concursos_publicos
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
            WHERE tipo_procedimento = 'Concurso público' AND contratos_basegov."id" > %s
            ORDER BY data_publicacao DESC, id DESC;
            ''', (last_id,))
new_data = cur.fetchall()




# Inserir os valores extraidos na query anterior na tabela "concursos_publicos"
cur = conn.cursor()
for i in new_data:
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




# Atualizar colunas auxiliares da tabela concursos_publicos apenas para os novos IDs
# 1. Separar entidade_adjudicante em nome da entidade, NIF e URL
# 2. Mesmo procedimento para a coluna entidades_contratadas
# 3. Contar o número de entidades concorrentes
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
            WHERE concursos_publicos."id" > %s;
            ''', (last_id,))
conn.commit()




# Substituir entradas None por 1 na coluna nr_entidadesconcorrentes
cur = conn.cursor()
cur.execute('''
            UPDATE concursos_publicos
            SET nr_entidadesconcorrentes = COALESCE(nr_entidadesconcorrentes, 1)
            WHERE concursos_publicos."id" > %s;
            ''', (last_id,))
conn.commit()




# Caracterização dos contratos de acordo com o tipo de contrato : Empreitadas OU Bens e Serviços
# Guardar conjunto de IDs mais recentes e respetivos tipos de contrato da tabela contratos_basegov
cur = conn.cursor()
cur.execute('''
            SELECT id, concursos_publicos."contractTypes"
            FROM concursos_publicos
            WHERE concursos_publicos."id" > %s
            ORDER BY data_publicacao DESC, id DESC;
            ''', (last_id,))
tcs = cur.fetchall()




# Caracterizar cada um dos novos IDs relativamente ao tipo de contrato
# Percorrer cada um dos IDs mais recentes
# i[0] = ID
# i[1] = tipo de contrato
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
        
        




# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- CÁLCULO DAS FLAGS  ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #


# Guardar conjunto de IDs mais recentes da tabela contratos_basegov desde o último ID analisado
cur = conn.cursor()
cur.execute('''
            SELECT
                contratos_basegov."id",
                contratos_basegov."data_publicacao"
            FROM contratos_basegov
            WHERE tipo_procedimento = 'Concurso público' AND contratos_basegov."id" > %s
            ORDER BY data_publicacao DESC, id DESC;;
            ''', (last_id,))
new_ids = cur.fetchall()




# Escrever valores dos IDs de ontem na tabela
# Inicialmente, definir o valor das flags binárias como false
# Nos passos seguintes, os contratos com flag ativada da tabela table_temp serão atualizados
cur = conn.cursor()
for i,j in new_ids:
    cur.execute(''' INSERT INTO table_temp(id, data_publicacao, "R003", "R018", "RF2", "RF3") 
                    VALUES (%s, %s, false, false, false, false)
                ;''', (i,j)) 
conn.commit() 




# Aplicar flag R003 ao novo conjunto de IDs 
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "R003" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id" 
                FROM contratos_basegov
                JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                WHERE contratos_basegov."id" > %s AND 
                    (concursos_publicos."tipo_contrato" = 'Empreitadas' AND contratos_basegov."anuncio_proposalDeadline" < 14) 
                    OR
                    (concursos_publicos."tipo_contrato" = 'Bens e Serviços' AND contratos_basegov."anuncio_proposalDeadline" < 6)
            );
            ''', (last_id,))
conn.commit() 




# Aplicar flag R018 ao novo conjunto de IDs 
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "R018" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id"
                FROM contratos_basegov
                JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                WHERE contratos_basegov."id" > %s AND concursos_publicos."nr_entidadesconcorrentes" = 1
	        );''', (last_id,))
conn.commit() 





# Aplicar flag RF2 ao novo conjunto de IDs 
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "RF2" = true
            WHERE table_temp."id" IN (
                SELECT contratos_basegov."id" 
                FROM contratos_basegov
                WHERE contratos_basegov."id" > %s AND tipo_procedimento = 'Concurso público' 
                    AND TO_CHAR(contratos_basegov."anuncio_drPublicationDate", 'MM-DD') 
                    IN ('01-01', '04-25', '05-01', '06-10', '08-15','10-05', '11-01', '12-01', '12-08', '12-25')
            );''', (last_id,))
conn.commit() 




# Aplicar flag RF3 ao novo conjunto de IDs 
cur = conn.cursor()
cur.execute('''
            UPDATE table_temp
            SET "RF3" = true
            WHERE table_temp."id" IN (
            SELECT contratos_basegov."id" 
                FROM contratos_basegov 
                WHERE contratos_basegov."id" > %s AND contratos_basegov."totalEffectivePrice" > 0 AND ABS(contratos_basegov."totalEffectivePrice" - preco_contratual) > 0
                );
            ''', (last_id,))
conn.commit() 
