# Packages
import psycopg2
import os


import flag_calculator


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



# Script auxiliar para o caso em que o script principal - process_update.py - não é executado corretamente
# Se existerem valores NULL na coluna de verification da tabela daily_flags, significa que o script não correu
# como deveria e, como tal, existem contratos em que não foram aplicados as funções das redflags
# 
# Assim, o primeiro passo é remover os respetivos contratos associados às entradas NULL da coluna verificação
# Posteriormente, irá ser atualizada a tabela com os contratos não calculados corretamente MAIS os contratos
# que, entretanto, foram adicionados à tabela 'mãe' da base de dados


def null_verification():
    """
    Função que verifica se existem, ou não, entradas NULL na coluna verification
    Se não existir nenhuma entrada NULL significa que não houve erros no procesamento do scritp e, como tal,
        o processo segue como deveria

    Por outro lado, se existirem entradas NULL são retornados todos os IDs - no formato de tuplo - de contratos associados
    a essas mesmas entradas para serem, posteriormente, removidos da tabela daily_flags
    """
    cur = conn.cursor()
    cur.execute('''
                SELECT daily_flags."id"
                FROM daily_flags
                WHERE verification IS NULL
                ORDER BY data_publicacao ASC, daily_flags."id" ASC
                ;
                ''')
    
    result = cur.fetchall()
    
    if len(result) == 0:
        return(None)
    else:
        return(tuple(result))




def last_nonnull():
    """
    Função que retorna o último ID da tabela auxiliar 'daily_flags' cujo valor da coluna verification é NOT NULL
    Esta função não irá ser utilizada. Fez parte de uma abordagem para resolver o problema
    """
    cur = conn.cursor()
    cur.execute('''
                SELECT daily_flags."id"
                FROM daily_flags
                WHERE verification IS NOT NULL
                ORDER BY data_publicacao DESC, daily_flags."id" DESC;
                ''')
    return(cur.fetchone()[0])



def remove_null(ids_contrato):
    """
    Função que remove todos os contratos cujas entradas da coluna verification toma o valor NULL
    O parâmetro de entrada é o tuplo de IDs retornado pela função null_verification()
    """
    cur = conn.cursor()
    cur.execute('''
                DELETE FROM daily_flags
                WHERE daily_flags."id" IN %s;
                ''', (ids_contrato,))
    conn.commit() 


