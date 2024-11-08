# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- CÁLCULO DAS FLAGS  ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

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


# Lista de flags calculadas:
# 1. R003 - Short period of time for bidders to submit interest 
# 2. R017 - Unreasonably high or low line item
# 3. R018 - Single bid receive
# 4. R019 - Low number of bidders for item and procuring entity
# 5.  RF2 - Publicação do anúncio em DR num feriado
# 6.  RF3 - Alteração do preço contratual após celebração do contrato


def lastid():

    """
    Função que retorna o último ID copiado para a tabela auxiliar 'daily_flags'
    A obtenção deste ID tem em conta que o script correu sem problemas, os contratos foram atualizados
    na tabela 'concursos_publicos' e as flags foram todas calculadas corretamente e, consequentemente,
    todas as entradas da coluna verification são igual a true
    """

    cur = conn.cursor()
    cur.execute('''
                SELECT daily_flags."id"
                FROM daily_flags
                ORDER BY data_publicacao DESC, daily_flags."id" DESC
                LIMIT 1;
                ''')
    return(cur.fetchone()[0])



def id_colector(id_contrato):

    """
    Função que retorna o conjunto de todos os novos IDs e as respetivas datas de publicação
     
    Parâmetro de entrada  
        id_contrato : último ID processado / ID mais recente da tabela 'concursos_publicos'

    return: 
        lista de todos os novos IDs, desde o último processado até ao mais recente
    """

    cur = conn.cursor()
    cur.execute('''
                SELECT
                    contratos_basegov."id",
                    contratos_basegov."data_publicacao"
                FROM contratos_basegov
                WHERE tipo_procedimento = 'Concurso público' AND contratos_basegov."id" > %s
                ORDER BY data_publicacao DESC, id DESC;
                ''', (id_contrato,))
    return(cur.fetchall())




def default_table(ids_recentes):
    
    """
    Função que insere, na tabela final 'daily_flags' a lista dos novos IDs e datas recolhidos.
    Por default, vai atribuir também a cada uma das flags o valor false. Posteriormente, 
    será aplicada cada uma das flags aos novos contratos e, na eventualidade de a flag ser disparada,
    o valor da coluna para o respetivo contrato passa a ser true

    Parâmetro de entrada  
        lista de todos os novos IDs, desde o último processado até ao mais recente
    """
    
    cur = conn.cursor()
    for i,j in ids_recentes:
        cur.execute(''' 
                    INSERT INTO daily_flags(id, data_publicacao,"RF2", "RF3", "R003", "R017", "R018", "R019") 
                    VALUES (%s, %s, false, false, false, false, false, false);
                    ''', (i,j)) 
    conn.commit() 




def flag_r003(id_contrato):

    """
    Verificação dos prazos de apresentação de proposta consoante o tipo de contrato
    Baseado no artigo 135.º do CCP e nas diretrizes da OCP
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "R003" = true
                WHERE daily_flags."id" IN (
                    SELECT contratos_basegov."id" 
                    FROM contratos_basegov
                    JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                    WHERE contratos_basegov."id" > %s AND 
                        (concursos_publicos."tipo_contrato" = 'Empreitadas' AND contratos_basegov."anuncio_proposalDeadline" < 14) 
                        OR
                        (concursos_publicos."tipo_contrato" = 'Bens e Serviços' AND contratos_basegov."anuncio_proposalDeadline" < 6)
                );
                ''', (id_contrato,))
    conn.commit() 




def flag_r018(id_contrato):
    
    """
    Verificação de todos os concursos públicos em que haja apenas uma entidade concorrente 
    """
    
    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "R018" = true
                WHERE daily_flags."id" IN (
                    SELECT contratos_basegov."id"
                    FROM contratos_basegov
                    JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                    WHERE contratos_basegov."id" > %s AND concursos_publicos."nr_entidadesconcorrentes" = 1
                );''', (id_contrato,))
    conn.commit() 





def flag_rf2(id_contrato):

    """
    Verificação de todos os concursos públicos cujo anúncio seja publicado em DR num feriado
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "RF2" = true
                WHERE daily_flags."id" IN (
                    SELECT contratos_basegov."id" 
                    FROM contratos_basegov
                    WHERE contratos_basegov."id" > %s AND tipo_procedimento = 'Concurso público' 
                        AND TO_CHAR(contratos_basegov."anuncio_drPublicationDate", 'MM-DD') 
                        IN ('01-01', '04-25', '05-01', '06-10', '08-15','10-05', '11-01', '12-01', '12-08', '12-25')
                );''', (id_contrato,))
    conn.commit() 




def flag_rf3(id_contrato):

    """
    Verificação dos contratos que sofreram alterações ao preço contratual após celebração do contrato
    (Derrapagens)
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "RF3" = true
                WHERE daily_flags."id" IN (
                SELECT contratos_basegov."id" 
                    FROM contratos_basegov 
                    WHERE contratos_basegov."id" > %s AND contratos_basegov."totalEffectivePrice" > 0 AND ABS(contratos_basegov."totalEffectivePrice" - preco_contratual) > 0
                    );
                ''', (id_contrato,))
    conn.commit() 




def flag_r017(id_contrato, upper, lower):

    """
    Verificar se o preço contratual de um determinado contrato, de acordo com a respetiva categoria
    ( categorizaçao feita de todos os contratos tendo em conta os primeiros 3 dígitos do CPV)
    se encontra dentro de um intervalo definido pelo upper e lower limit
    O upper e lower limit são definidos como SQL queries e, para já, são definidos através
    da constante de Medcouple ( outliers ) com algumas alterações no parâmetro 1.5
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "R017" = true
                WHERE daily_flags."id" IN (
                    SELECT  contratos_basegov."id"
                    FROM contratos_basegov 
                    JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                    JOIN precoc_stat ON SUBSTRING(contratos_basegov."cpv", 1, 3) = precoc_stat."cpv"
                    WHERE contratos_basegov."id" > %s AND 
                        ({lim_sup} OR {lim_inf})
                    );
                    '''.format(lim_sup=upper, lim_inf=lower), (id_contrato,))
    conn.commit() 




def flag_r019(id_contrato, upper, lower):

    """
    Verificar se o número de empresas que se candidatam a um determinado contrato, de acordo com a respetiva categoria
    ( categorizaçao feita de todos os contratos tendo em conta os primeiros 2 dígitos do CPV)
    se encontra dentro de um intervalo definido pelo upper e lower limit
    O upper e lower limit são definidos como SQL queries e, para já, são definidos através
    da constante de Medcouple ( outliers ) com algumas alterações no parâmetro 1.5
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "R019" = true
                WHERE daily_flags."id" IN (
                    SELECT  contratos_basegov."id"
                    FROM contratos_basegov 
                    JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"
                    JOIN cpv_stat ON SUBSTRING(contratos_basegov."cpv", 1, 2) = cpv_stat."cpv"
                    WHERE contratos_basegov."id" > %s AND 
                        ({lim_sup} OR {lim_inf}));
                    '''.format(lim_sup=upper, lim_inf=lower), (id_contrato,))
    conn.commit() 




def verification(id_contrato):

    """
    Esta função é um mecanismo de 'segurança'
    Caso todas as flags sejam calculadas corretamente, na tabela daily_flags, é atribuído a cada contrato
    o valor de true na coluna verification.
    Se as flags não forem calculadas corretamente devido a algum erro - do servidor, por exemplo - o valor
    da coluna irá manter-se NULL
    Assim, antes de correr o script para preencher a tabela daily_flags é preciso primeiro verificar
    se existem entradas NULL na coluna verification. Caso existam, é preciso recalcular as flags. 
    Após recalcular, é necessário atualizar com os novos contratos. Estes dois passos podem ser feitos 
    em simultâneo, como irá ser explicado no script process_update.py
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE daily_flags
                SET "verification" = true
                WHERE daily_flags."id" > %s;
                ''', (id_contrato,))
    conn.commit() 






def main(last_id):

    """
    Função principal que calcula todas as flags

    São criadas variáveis inicias de sucesso ou insucesso relativamente ao cálculo das flags.
    Por default, é atribuído valor true pois parte-se do princípio que o script corre sem falhas

    De seguida são calculadas as flags. Caso haja alguma falha, é atribuído à variável de 
    sucesso de flag o valor false

    Por fim, são verificas se todos os valores de sucesso são true
    Se todos forem true, é aplicada a função verification : o script correu como devia
    Caso contrário, não acontece nada. A coluna verification continua NULL
    Esta verificação é apenas vantajosa no caso em que o cálculo de alguma flag tem um bug
    No caso em que o script não corre por causa de alguma falha externa ao código, esta verificação
    da linha if-else também não é executada
    """

    # Status de sucesso 
    # Caso a função não corra, é atribuído o valor False 
    flag_r003_success = True
    flag_r018_success = True
    flag_rf2_success = True
    flag_rf3_success = True
    flag_r017_success = True
    flag_r019_success = True

    try:
        flag_r003(last_id)
    except Exception as e:
        print(f"Error running flag_r003: {e}")
        flag_r003_success = False
    
    try:
        flag_r018(last_id)
    except Exception as e:
        print(f"Error running flag_r018: {e}")
        flag_r018_success = False
    
    try:
        flag_rf2(last_id)
    except Exception as e:
        print(f"Error running flag_rf2: {e}")
        flag_rf2_success = False
    
    try:
        flag_rf3(last_id)
    except Exception as e:
        print(f"Error running flag_rf3: {e}")
        flag_rf3_success = False
    


    lim_inf_mc = " contratos_basegov.""preco_contratual"" <= precoc_stat.""lower_fence"" "
    lim_sup_mc = " contratos_basegov.""preco_contratual"" >= precoc_stat.""upper_fence"" " 
    try:
        flag_r017(last_id, lim_sup_mc, lim_inf_mc)
    except Exception as e:
        print(f"Error running flag_r017: {e}")
        flag_r017_success = False



    lim_inf19 = " concursos_publicos.""nr_entidadesconcorrentes"" >= cpv_stat.""upper_fence"" "
    lim_sup19 = " concursos_publicos.""nr_entidadesconcorrentes"" <= cpv_stat.""lower_fence"" "    
    try:
        flag_r019(last_id, lim_sup19, lim_inf19)
    except Exception as e:
        print(f"Error running flag_r019: {e}")
        flag_r019_success = False

    #flag_r003_success = False

    if flag_r003_success and flag_r018_success and flag_rf2_success and flag_rf3_success and flag_r017_success and flag_r019_success:
        verification(last_id)
    else:
        pass


# if __name__ == "__main__":
#     last_id = lastid()
#     new_ids = id_colector(last_id)
#     default_table(new_ids)    
#     main(last_id)