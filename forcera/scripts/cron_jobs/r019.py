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




def flag_r19(dia, lim1, lim2):
    """
    Parâmetros de entrada:
        dia : data do dia de ontem no formato YYYY-MM-DD
        lim1 : query para secção WHERE : limite superior ( ou inferior )
        lim2 : query para secção WHERE : limite inferior ( ou superior )

    return:
        ids de ontem que se encontrem além das fronteiras definidas pelas queries definidas em lim1 e lim2
    """


    cur = conn.cursor()
    query = f"""
            SELECT  contratos_basegov."id"
                    --concursos_publicos."nr_entidadesconcorrentes", 
                    --cpv_stat."mean", 
                    --cpv_stat."q3" + 3*cpv_stat."dq" AS lim_superior,  
                    --cpv_stat."q1" - 3*cpv_stat."dq" AS lim_inferior,
                    --cpv_stat."q1",
                    --cpv_stat."q2",
                    --cpv_stat."q3"

            FROM contratos_basegov 

            JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"

            JOIN cpv_stat ON SUBSTRING(contratos_basegov."cpv", 1, 2) = cpv_stat."cpv"

            WHERE   contratos_basegov."data_publicacao" = %s AND 
                    ({lim1} OR {lim2});
            """

    cur.execute(query, (dia,))
    result = cur.fetchall()
    
    return result





# DEFINIÇÃO DOS DIFERENTES LIMITES

# OUTLIER MODERADO
outmod_sup = " concursos_publicos.""nr_entidadesconcorrentes"" > cpv_stat.""q3"" + 1.5*cpv_stat.""dq"" "
outmod_inf = " concursos_publicos.""nr_entidadesconcorrentes"" < cpv_stat.""q1"" - 1.5*cpv_stat.""dq"" " 

# OUTLIER SEVERO
outsev_sup = " concursos_publicos.""nr_entidadesconcorrentes"" > cpv_stat.""q3"" + 3*cpv_stat.""dq"" "
outsev_inf = " concursos_publicos.""nr_entidadesconcorrentes"" < cpv_stat.""q1"" - 3*cpv_stat.""dq"" " 

# OUTLIER : MÉTODO CONSTANTE DE MEDCOUPLE
outmc_sup = " concursos_publicos.""nr_entidadesconcorrentes"" > cpv_stat.""upper_fence"" "
outmc_inf = " concursos_publicos.""nr_entidadesconcorrentes"" < cpv_stat.""lower_fence"" " 

# LIMITE PARAMETRIZÁVEL
lim_inf = " concursos_publicos.""nr_entidadesconcorrentes"" < INSERIR VALOR "
lim_sup = " concursos_publicos.""nr_entidadesconcorrentes"" > INSERIR VALOR " 




for i,j in enumerate(flag_r19(ontem,outmc_inf, outmc_sup)):
    print(i,j)