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
yesterday = datetime.now() - timedelta(4)
ontem = datetime.strftime(yesterday, '%Y-%m-%d')



def flag_r17(dia, lim_sup, lim_inf):
    """
    Parâmetros de entrada:
        dia : data do dia de ontem no formato YYYY-MM-DD
        lim1 : query para secção WHERE : limite superior ( ou inferior )
        lim2 : query para secção WHERE : limite inferior ( ou superior )

    return:
        ids de ontem que se encontrem além das fronteiras definidas pelas queries definidas em lim_inf e lim_sup
    """


    cur = conn.cursor()
    query = f"""
            SELECT  contratos_basegov."id"
                    --contratos_basegov."preco_contratual", 
                    --precoc_stat."mean", 
                    --precoc_stat."q3" + 3*precoc_stat."dq" AS lim_superior,  
                    --precoc_stat."q1" - 3*precoc_stat."dq" AS lim_inferior,
                    --precoc_stat."q1",
                    --precoc_stat."q2",
                    --precoc_stat."q3"

            FROM contratos_basegov 

            JOIN concursos_publicos ON contratos_basegov."id" = concursos_publicos."id"

            JOIN precoc_stat ON SUBSTRING(contratos_basegov."cpv", 1, 3) = precoc_stat."cpv"

            WHERE   contratos_basegov."data_publicacao" = %s AND 
                    ({lim_sup} OR {lim_inf});
            """

    cur.execute(query, (dia,))
    result = cur.fetchall()
    
    return result




# DEFINIÇÃO DOS DIFERENTES LIMITES

# OUTLIER MODERADO
outmod_inf = " contratos_basegov.""preco_contratual"" > precoc_stat.""q3"" + 1.5*precoc_stat.""dq"" "
outmod_sup = " contratos_basegov.""preco_contratual"" < precoc_stat.""q1"" - 1.5*precoc_stat.""dq"" " 

# OUTLIER SEVERO
outsev_inf = " contratos_basegov.""preco_contratual"" > precoc_stat.""q3"" + 3*precoc_stat.""dq"" "
outsev_sup = " contratos_basegov.""preco_contratual"" < precoc_stat.""q1"" - 3*precoc_stat.""dq"" " 

# OUTLIER : MÉTODO CONSTANTE DE MEDCOUPLE
outmc_inf = " contratos_basegov.""preco_contratual"" < precoc_stat.""lower_fence"" "
outmc_sup = " contratos_basegov.""preco_contratual"" > precoc_stat.""upper_fence"" " 

# LIMITE PARAMETRIZÁVEL
lim_inf = " contratos_basegov.""preco_contratual"" < INSERIR_VALOR "
lim_sup = " contratos_basegov.""preco_contratual"" > INSERIR_VALOR " 




for i,j in enumerate(flag_r17(ontem,outmod_inf, outmod_sup)):
    print(i,j)
