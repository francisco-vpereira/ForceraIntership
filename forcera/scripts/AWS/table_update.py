# -------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------ UPDATE DA TABELA AUXILIAR *concursos_publicos* -------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

# Packages
import psycopg2
import os



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




def lastid():
    """
    Função que retorna o último ID copiado para a tabela auxiliar 'concursos_publicos'
    """
    cur = conn.cursor()
    cur.execute('''
                SELECT
                    concursos_publicos."id"
                FROM concursos_publicos
                ORDER BY data_publicacao DESC, concursos_publicos."id" DESC
                LIMIT 1;
                ''')
    return(cur.fetchone()[0])




def new_contracts(id_contrato):

    """
    Função que retorna todos os contratos, desde o mais recente até ao id_contrato, considerando apenas as colunas
        selecionadas na query. Estes dados são, posteriormente, copiados para a tabela 'concursos_publicos'

    Parâmetro de entrada  
        id_contrato : último ID processado / ID mais recente da tabela 'concursos_publicos'
    """
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
                    contratos_basegov."executionPlace",
                    contratos_basegov."cpv"
                FROM contratos_basegov
                WHERE tipo_procedimento = 'Concurso público' AND contratos_basegov."id" > %s
                ORDER BY data_publicacao DESC, id DESC;
                ''', (id_contrato,))
    return(cur.fetchall())





def write_contracts(contracts):
    """
    Função que insere contratos na tabela auxiliar 'concursos_publicos' nas colunas correspondentes

    Parâmetro de entrada:
        contracts : Conjunto de contratos que se pretende copiar para a tabela 'concursos públicos'
    """
    cur = conn.cursor()
    for i in contracts:
        cur.execute('''
                    INSERT INTO concursos_publicos(
                        id,
                        data_publicacao,
                        "contractTypes",
                        fundamentacao,
                        entidade_adjudicante,
                        entidades_contratadas,
                        entidades_concorrentes,
                        "executionPlace",
                        cpv
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                ''', i)
    conn.commit()




def update_columns(id_contrato):

    """
    Função que calcula os parâmetros das colunas adicionais da tabela auxiliar
    1. Separar entidade_adjudicante em nome da entidade, NIF e URL
    2. Mesmo procedimento para a coluna entidades_contratadas
    3. Contar o número de entidades concorrentes
    Estes parâmetros serão utilizados para calcular algumas flags

    O split das strings ( ponto 1.) foi atualizado dado que existe uma inconsistência de preenchimento no portal Base. 
    Por vezes, quando os contratos são inseridos são feitos de uma de duas formas :

    Centro Hospitalar Universitário Lisboa Central, E. P. E. (508080142)(https://www.base.gov.pt/Base4/pt/detalhe/?type=entidades&id=41882)
    Centro Hospitalar Universitário de Lisboa Central, E.P.E. (CHULC) (508080142)(https://www.base.gov.pt/Base4/pt/detalhe/?type=entidades&id=41882)

    As regular expression usadas fazem a busca do fim da string para o início. Começam pelo URL, de seguida extraem o NIF e, 
    só por fim, o nome da entidade. 

    Parâmetro de entrada
        id_contrato: último ID processado / ID mais recente da tabela 'concursos_publicos'
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE concursos_publicos
                SET 
                    url1 = substring(entidade_adjudicante from '\((https?://[^)]+)\)'),
                    nif1 = substring(entidade_adjudicante from '\((\w+)\)\(https?://.*?\)'),
                    adjudicante = substring(entidade_adjudicante from '^\s*([^()]+) '),
                    url2 = substring(entidades_contratadas from '\((https?://[^)]+)\)'),
                    nif2 = substring(entidades_contratadas from '\((\w+)\)\(https?://.*?\)'),
                    adjudicataria = substring(entidades_contratadas from '^\s*([^()]+) '),
                    nr_entidadesconcorrentes = CARDINALITY(STRING_TO_ARRAY(entidades_concorrentes, '|||')) + 1
                WHERE concursos_publicos."id" > %s;
                ''',(id_contrato,))
    conn.commit()



def update_null_nif1(id_contrato):
    """
    Função que volta a fazer split da coluna entidade_adjudicante quando o split não é executado como deveria na função
    update_columns e o valor da coluna nif1 é NULL. Este script é utilizado para quando

    World Medica, S.L. (ESB82612599)(https://www.base.gov.pt/Base4/pt/detalhe/?type=entidades&id=399066)
    """
    
    cur = conn.cursor()
    cur.execute('''
                UPDATE concursos_publicos
                SET 
                    url1 = substring(entidade_adjudicante from '\((https?://[^)]+)\)'),
                    nif1 = substring(entidade_adjudicante from '\((\w+)\)\(https?://.*?\)'),
                    adjudicante = substring(entidade_adjudicante from '^\s*([^()]+) ')
                WHERE nif1 IS NULL AND concursos_publicos."id" > %s;
                ''',(id_contrato,))
    conn.commit()


def update_null_nif2(id_contrato):
    cur = conn.cursor()
    cur.execute('''
                UPDATE concursos_publicos
                SET 
                    url2 = substring(entidades_contratadas from '\((https?://[^)]+)\)'),
                    nif2 = substring(entidades_contratadas from '\((\w+)\)\(https?://.*?\)'),
                    adjudicataria = substring(entidades_contratadas from '^\s*([^()]+) ')
                WHERE nif2 IS NULL AND concursos_publicos."id" > %s;
                ''',(id_contrato,))
    conn.commit()


def nec_null(id_contrato):
    
    """
    Por default, sempre que, para um determinado concurso público só se candidata uma entidade, a coluna de entidades concorrentes não é
    preenchida, contendo a string None. Assim, para todos os contratos cuja entrada da coluna nr_entidadesconcorrentes seja None, insere-se
    o valor 1.

    Parâmetro de entrada
        id_contrato: último ID processado / ID mais recente da tabela 'concursos_publicos'
    """

    cur = conn.cursor()
    cur.execute('''
                UPDATE concursos_publicos
                SET nr_entidadesconcorrentes = COALESCE(nr_entidadesconcorrentes, 1)
                WHERE concursos_publicos."id" > %s;
                ''', (id_contrato,))
    conn.commit()




def contract_type(id_contrato):

    """
    Função que caracteriza os contratos de acordo com o tipo de contrato : Empreitadas OU Bens e Serviços

    Parâmetro de entrada
        id_contrato: último ID processado / ID mais recente da tabela 'concursos_publicos'
    
    return:
        Conjunto de IDs mais recentes e respetivos tipos de contrato da tabela contratos_basegov
    """

    cur = conn.cursor()
    cur.execute('''
                SELECT id, concursos_publicos."contractTypes"
                FROM concursos_publicos
                WHERE concursos_publicos."id" > %s
                ORDER BY data_publicacao DESC, id DESC;
                ''', (id_contrato,))
    return(cur.fetchall())




def tipocontrato_classifier(tcs):
    
    """
    O tipo de contrato vai ser classificado em Empreitadas OU Bens e Serviços consoante apareça,
    ou não, a palavra 'obra' na sua descrição

    Parâmetro de entrada
        tcs: (tipos de contratos) consiste no output da função contract_type. É o conjunto de IDs
        e respstivo tipo de contrato.
    """

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




# # Correr as funções

# # Obter último ID processado 
# last_id = lastid()

# # Guardar novos contratos e colunas significativas
# contratos = new_contracts(last_id)

# # Copiar novos contratos para a tabela concursos_publicos
# write_contracts(contratos)

# # Dar update às colunas auxiliares que foram construídas
# update_columns(last_id)

# # Susbtituir entradas None por 1 da coluna nr_entidadesconcorrentes
# nec_null(last_id)

# # Classificação dos contratos consoante o tipo
# # Guardar IDs dos novos contratos e respetivo tipo
# tcontratos = contract_type(last_id)

# # Classificação dos novos contratos, em 2 categorias, consoante o tipo
# tipocontrato_classifier(tcontratos)
