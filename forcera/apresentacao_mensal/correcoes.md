# Correções Apresentação


- **Slide 3** : Incluir Python e JupyterNotebook nas ferramentas utilizadas

- **Slide 4** : Dar mais ênfase sobre trabalho desenvolvido pela OCP. Desenvolver mais

- **Slide 6** : Arranjar uma maneira melhor de apresentar a folha de excel que contém as flags - o que é que cada coluna contém, como está estruturada. Relativamente à escolha das flags, justificar o que foi feito durante o processo de seleção das flags pela facilidade de implementação e do valor da flag ( escala utilizada )

- **Slide 7** : Fazer uma breve introdução às flags antes de começar a apresentação

- **Slide 10** : Optar por um plot com maior representatividade

- **Slide 12** : Dar nomes específicos às funções. Não incluir a parte dos lotes dado que não temos acesso aos preços base por lote. Dessa forma, o resultado que estamos a obter não é fidedigno. 

- **Slide 18** : Relativamente aos contratos com preço contratual negativo : verificar, a partir do contrato em pdf no basegov, se de facto é apenas um lapso na introdução do preço e é colocado um sinal - a mais. Caso se verifique isso na maioria dos contratos analisados, substituir todos os valores negativos pelo valor absoluto. Relativamente aos contratos cujo preço contratual é zero : podem ser ignorados para já. 


Correções Gerais : 

- Não fazer uma descrição tão detalhada do processo de construção de todas as flags

- Incluir alguns casos reais : mostrar contratos em que não seja e outros em que seja ativada a flag para provar que o código funciona. Mostrar resultados

Trabalho futuro : 

- Criar um script python que, automaticamente, corra todos os indicadores nos contratos da base de dados

    - Primeiro passo : fazer isso para o conjunto de contratos históricos
    - Segunda passo : criar um script que faça isso para todos os contratos novos que são adicionados diariamente à base de dados 
