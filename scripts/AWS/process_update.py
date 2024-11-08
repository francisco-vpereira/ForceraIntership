# Packages
import psycopg2
import os


import table_update
import flag_calculator
import none_cases


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


def lambda_handler(event, context):
    try:
        main_process()
    except Exception as e:
        print(f"Error running script : {e}")

    


def main_process():

    # -------------------------------------------------------------------------------------------------------------------- #
    # ------------------------------------ UPDATE DA TABELA AUXILIAR *concursos_publicos* -------------------------------- #
    # -------------------------------------------------------------------------------------------------------------------- #


    # Obter último ID processado 
    last_id = table_update.lastid()

    # Guardar novos contratos e colunas significativas
    contratos = table_update.new_contracts(last_id)

    # Copiar novos contratos para a tabela concursos_publicos
    table_update.write_contracts(contratos)

    # Dar update às colunas auxiliares que foram construídas
    table_update.update_columns(last_id)

    # Susbtituir entradas None por 1 da coluna nr_entidadesconcorrentes
    table_update.nec_null(last_id)

    # Classificação dos contratos consoante o tipo
    # Guardar IDs dos novos contratos e respetivo tipo
    tcontratos = table_update.contract_type(last_id)

    # Classificação dos novos contratos, em 2 categorias, consoante o tipo
    table_update.tipocontrato_classifier(tcontratos)

    print("Tabela ConcursosPúblicos preenchida")


    # -------------------------------------------------------------------------------------------------------------------- #
    # ------------------------------------------------- CÁLCULO DAS FLAGS  ----------------------------------------------- #
    # -------------------------------------------------------------------------------------------------------------------- #

    # Se houver valores None na coluna verificação, significa que nem todas as flags foram calculadas para os novos contratos
    # Nesse caso é preciso voltar a calcular
    # Caso contrário, o processo segue normalmente



    # Variável que toma 2 possíveis valores :
    # None caso não existam entradas NULL da coluna verification ( processo correu de forma corretamente da última vez )
    # tuplo de IDs associados a entradas NULL da coluna verification ( processo não terminou da última vez / correu com erros )
    none_number = none_cases.null_verification()



    if none_number == None:
        #print('Sem valores nulos', none_number)
        # Último ID copiado para a tabela daily_flags

        latest_id = flag_calculator.lastid()
        new_ids = flag_calculator.id_colector(latest_id)
        flag_calculator.default_table(new_ids)    
        flag_calculator.main(latest_id)



    else:
        #print('Existem valores nulos. \nPrimeiro ID com valor nulo: ', tuple(none_number), len(none_number))
        none_cases.remove_null(none_number) 
        latest_id = flag_calculator.lastid()
        new_ids = flag_calculator.id_colector(latest_id)
        flag_calculator.default_table(new_ids)    
        flag_calculator.main(latest_id)