# Descrição Tabelas da Base de Dados

1. **ajustes_diretos**

Tabela construída a partir do script *ajustes_diretos*. Contém as colunas necessárias para o cálculo das flags RF1


2. **ajustesdiretos**

Foi uma versão preliminar da tabela anterior. Não é usada e pode ser apagada. 


3. **concursos_publicos**

Tabela construída a partir do script *concursos_publicos*. Contém todas as colunas necessárias para calcular as flags R003, R017, R018, R019, RF2 e RF3. É preciso realizar algumas operações sobre os valores de algumas colunas a fim de extrair informação : separação das colunas entidade adjudicante, contagem do número de entidades concorrentes na coluna entidades\_concorrentes, ...


4. **concursospublicos**

É uma versão preliminar da tabela anterior e foi construída a partir do script *concursospublicos*. Não é usada e pode ser apagada. 

5. **contratos_basegov**

Tabela que contém a totalidade dos anúncios. 


6. **cpv_stat**

Tabela auxiliar para calcular flag R019. Contém indicadores estatísticos para todas as categorias de dois dígitos do CPV referentes ao número de entidades concorrentes.


7. **cpv_stat1**

Análogo ao caso anterior, mas podem mais um nível de particularidade : tipo de contrato ( Bens e Serviços OU Empreitadas ). Não é utilizada. 


8. **precoc_stat**

Tabela auxilar para calcular flag R017. Contém indicadores estatísticos para todas as categorias de 3 dígitos do CPV referentes ao preço contratual. 


9. **table_temp**

Tabela que vai sendo atualizada diariamente com os novos contratos e vai calculando as respetivas flags. 

