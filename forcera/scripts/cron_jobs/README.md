# Calcular flags booleanas diariamente ( Versão de teste )

Todos os dias, este script vai atualizar duas tabelas : 

- uma tabela chamada, temporariamente, *table_temp*
- uma tabela auxiliar : *concursos\_publicos*


<br>
<br>


A tabela *table\_temp* é composta pelas seguintes colunas : 

- id : identificador do anúncio
- data\_publicacao : data de publicação do contrato na plataforma Basegov
- R003 : Tempo de submissão de propostas inferior ao valor definido no Artigo 135.º. É preciso ter em conta o tipo de contrato : Aquisição de Bens e Serviços OU Empreitadas
    - Tabela Auxiliar : *concursos\_publicos*
        - Coluna Auxiliar : tipo\_contrato
- R018 : Contratos com apenas uma entidade concorrente
    - Tabela Auxiliar : *concursos\_publicos*
        - Coluna Auxiliar : nr\_entidadesconcorrentes
- RF2 : Verificar se data de publicação de anúncio coincide com feriado nacional
- RF3 : Verificar se houve alterações ao preço contratual após celebração do contrato


<br>
<br>


A tabela *concursos\_publicos* é usada para obter informação que não vem discriminada na tabela original. Da tabela original, *contratos_basegov*, são copiadas as seguintes colunas para esta tabela : 

- id
- data\ _publicacao
- contractTypes
- fundamentacao
- entidade_adjudicante
- entidades_contratadas
- entidades_concorrentes
- executionPlace

As colunas calculadas construídas a partir das enunciadas no ponto anterior são :

- tipo\_contrato : coluna com dois valores : Bens e Serviços OU Empreitadas. Construída a partir da coluna contractTypes
- adjudicante : nome da entidade adjudicante. Contruída a partir da coluna entidade\_adjudicante
- nif1 : nif da entidade adjudicante. Construída a partir da coluna entidade\_adjudicante
- url1 : url que redireciona para página do Basegov onde são listados os contratos celebrados pela entidade adjudicante. Contruída a partir da coluna entidade\_adjudicante

- adjudicataria : nome da entidade adjudicaária. Contruída a partir da coluna entidades\_contratadas
- nif2 : nif da entidade adjudicatária. Construída a partir da coluna entidade\_contratadas
- url2 : url que redireciona para página do Basegov onde são listados os contratos celebrados pela entidade adjudicatária. Contruída a partir da coluna entidades\_contratadas
- nr\_entidadesconcorrentes : número de entidades que se candidatam a um determinado concurso público. Calculado a partir da coluna entidades\_concorrentes



# Processo : 

1. Determinar a data do dia de ontem no formato YYYY-MM-DD
2. Selecionar, a partir da tabela *contratos\_basegov* as colunas necessárias para preencher na tabela *concursos\_publicos* referentes ao dia de ontem (id, data\_publicacao, contractTypes, fundamentacao, entidade\_adjudicante, entidades_\contratadas, entidades\_concorrentes, executionPlace). 
3. Inserir esses valores na tabela *concursos\_publicos*
4. Dar update às colunas extra pertencentes à tabela *concursos\_publicos*
    - Primeiro são preenchidas as colunas : adjudicante, nif1, url1, adjudicataria, nif2, url2 nr\_entidadadesconcorrentes
5. Na coluna nr\_entidadesconcorrentes são substituídas as entradas sem nenhum valor por 1. Por default, nas entidades concorrentes não é inserida a informação relativamente à entidade vencedora. Caso só haja uma entidade a participar num determinado concurso, o valor da coluna entidades\_concorrentes irá ser nulo nesses casos. 
6. É feita a classificação do tipo de contrato e inserido o valor na coluna tipo\_contrato.
7. É adicionado à tabela *table_temp* os identificadores dos anúncios do dia de ontem e a respetiva data. É atribuído, também, a cada a flag o valor false. 
8. É aplicada a query da flag R003 ao conjunto de concursos públicos de ontem. Caso seja disparada uma flag, é feito um update na tabela *table\_temp*
9. Processo análogo para as restantes 3 flags


<br>
<br>

O cronjob é definido da seguinte forma: 

```
$ crontab -e 

# inserir este comando
0 9 * * * /home/francisco/MECAD/COMP/comp/bin/python3 /home/francisco/MECAD/2º\ Ano/Estágio/forcera/scripts/cron_jobs/daily_ids.py
```
