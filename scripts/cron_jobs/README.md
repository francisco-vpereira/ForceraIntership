***English version below.***

# Calcular flags booleanas diariamente 

Existem duas tabelas essencias na base de dados: 

- a tabela final: *daily_flags*
- uma tabela auxiliar: *concursos\_publicos*


<br>
<br>


A tabela *daily_flags* contém o produto final. Todos os dias são copiados os IDs dos novos concursos públicos publicados no Basgov e, posteriormente, aplicadas as flags construídas aos mesmos contratos. Todas as flags são booleanas. 

É composta pelas seguintes colunas : 

- id: identificador do anúncio
- data\_publicacao: data de publicação do contrato na plataforma Basegov
- verification: coluna com valor booleano. Se for true, script correu devidamente na última execução. Caso contrário, toma o valor false. É um mecanismo preventivo e irá ser explicado mais à frente. 
- R003: Tempo de submissão de propostas inferior ao valor definido no Artigo 135.º. É preciso ter em conta o tipo de contrato : Aquisição de Bens e Serviços OU Empreitadas
    - Tabela Auxiliar : *concursos\_publicos*
        - Coluna Auxiliar : tipo\_contrato
- R017: Preço inusual para determinada categoria. 
- R018: Contratos com apenas uma entidade concorrente
    - Tabela Auxiliar : *concursos\_publicos*
        - Coluna Auxiliar : nr\_entidadesconcorrentes
- R019: Número baixo de concorrentes
    - Tabelas Auxiliares: *concursos_publicos* e *precoc_stat*
- RF2: Verificar se data de publicação de anúncio coincide com feriado nacional
- RF3: Verificar se houve alterações ao preço contratual após celebração do contrato


<br>
<br>


A tabela *concursos\_publicos* é usada para obter informação que não vem discriminada na tabela original. Da tabela original, *contratos_basegov*, são copiadas as seguintes colunas para esta tabela : 

- id
- data\_publicacao
- contractTypes
- fundamentacao
- entidade_adjudicante
- entidades_contratadas
- entidades_concorrentes
- executionPlace
- cpv
- preco_contratual


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

1. Determinar o último ID da tabela *daily_flags* cujo valor da coluna verification seja true.  
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

***
 <br> 
 
# Calculate Daily Boolean Flags

There are two essential tables in the database:

- The final table: *daily_flags*
- An auxiliary table: *concursos\_publicos*


<br>
<br>


The *daily_flags* table contains the final product. Each day, the IDs of new public tenders published on Basgov are copied, and the constructed flags are subsequently applied to these contracts. All flags are boolean.

It is composed of the following columns:

- **id**: announcement identifier
- **data\_publicacao**: contract publication date on the Basegov platform
- **verification**: column with a boolean value. If true, the script ran successfully in the last execution; otherwise, it takes the value false. This is a preventive mechanism and will be explained later.
- **R003**: Proposal submission time is less than the value defined in Article 135. The contract type needs to be considered: Acquisition of Goods and Services OR Works.
    - **Auxiliary Table**: *concursos\_publicos*
        - **Auxiliary Column**: tipo\_contrato
- **R017**: Unusual price for a particular category.
- **R018**: Contracts with only one competing entity.
    - **Auxiliary Table**: *concursos\_publicos*
        - **Auxiliary Column**: nr\_entidadesconcorrentes
- **R019**: Low number of competitors.
    - **Auxiliary Tables**: *concursos_publicos* and *precoc_stat*
- **RF2**: Check if the publication date of the announcement coincides with a national holiday.
- **RF3**: Check if there were changes to the contractual price after the contract signing.


<br>
<br>


The *concursos\_publicos* table is used to obtain information not specified in the original table. From the original table, *contratos_basegov*, the following columns are copied to this table:

- **id**
- **data\_publicacao**
- **contractTypes**
- **fundamentacao**
- **entidade_adjudicante**
- **entidades_contratadas**
- **entidades_concorrentes**
- **executionPlace**
- **cpv**
- **preco_contratual**


The calculated columns built from those listed above are:

- **tipo\_contrato**: column with two values: Goods and Services OR Works. Built from the contractTypes column
- **adjudicante**: name of the awarding entity. Built from the entidade\_adjudicante column
- **nif1**: tax ID (NIF) of the awarding entity. Built from the entidade\_adjudicante column
- **url1**: URL redirecting to the Basegov page where contracts signed by the awarding entity are listed. Built from the entidade\_adjudicante column

- **adjudicataria**: name of the awarded entity. Built from the entidades\_contratadas column
- **nif2**: tax ID (NIF) of the awarded entity. Built from the entidades\_contratadas column
- **url2**: URL redirecting to the Basegov page where contracts signed by the awarded entity are listed. Built from the entidades\_contratadas column
- **nr\_entidadesconcorrentes**: number of entities that applied to a given public tender. Calculated from the entidades\_concorrentes column



# Process:

1. Determine the last ID in the *daily_flags* table where the verification column value is true.
2. Select from the *contratos\_basegov* table the necessary columns to populate in the *concursos\_publicos* table for the previous day (**id**, **data\_publicacao**, **contractTypes**, **fundamentacao**, **entidade\_adjudicante**, **entidades\_contratadas**, **entidades\_concorrentes**, **executionPlace**).
3. Insert these values into the *concursos\_publicos* table.
4. Update the extra columns belonging to the *concursos\_publicos* table:
    - First, populate the columns: **adjudicante**, **nif1**, **url1**, **adjudicataria**, **nif2**, **url2** **nr\_entidadesconcorrentes**.
5. In the **nr\_entidadesconcorrentes** column, replace empty entries with 1. By default, competitor entities do not include information regarding the winning entity. If only one entity participated in a given tender, the **entidades\_concorrentes** column value will be null in those cases.
6. Classify the contract type and insert the value in the **tipo\_contrato** column.
7. Add to the *table_temp* table the identifiers of announcements from the previous day along with their respective dates. Assign each flag a false value.
8. Apply the R003 flag query to the set of public tenders from the previous day. If a flag is triggered, update the *table\_temp* table.
9. Follow an analogous process for the remaining 3 flags.
