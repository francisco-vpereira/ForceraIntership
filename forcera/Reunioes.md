<h1><center> Reuniões Forcera </h1>


## Semana 1

1. Reunião 02/10/2023
- [ ] Ver tutorial de Git
- [ ] Ler e resumir manual : Red Flags for integrity
- [ ] Pesquisar acerca de red flags

2. Reunião 04/10/2023
- [ ] Continuar mesmas tarefas
- [ ] Começar a escrever
    - [ ] Organizar documento



## Semana 2

3. Reunião 11/10/2023

*Dúvidas* : 
- Título da tese/relatório é o que se encontra no plano de estágios ?
- Podemos criar as nossas próprias figuras/esquemas para tornar mais claro ? 

- [ ] Criar repositório no Github para ir adicionando resumos em .md
- [ ] Dar mais ênfase às etapas de Ternder, Award e Contract das estapas de procurement
- [ ] Ver sites sugeridos
- [ ] Classificar as flags da spreadsheet - tender award contract - de 2 maneiras : Facilidade de implementação e Valor da Flag. Numa fase inicial, começamos por implementar as flags com maior facilidade de implementação e maior valor. Aliar esta classificação com site do base-gov
- [ ] Definir bem *public procurement* e as *red flags* : não é só identificar fraude mas, também, detetar lapsos/erros


## Semana 3

4. Reunião 16/10/2023

- [ ] continuar a classificar flags

5. Reunião 18/10/2023

--- 

*Dúvidas :* 

- [x] Famalicão :  Neste [caso](https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=10296678) o preço contratual é 99.150,50€ e o preço base é 283.774,92 €. Isto quer dizer que a empresa que ganhou a licitação realizou uma proposta que pode ser executada por 99.150€ e o valor máximo que a entidade adjudicatária estaria disposta a pagar é 283.774 €? - **Sim**

- [ ] Relativamente à flag R007 : Unreasonable specifications (broad or too narrow ) - no caso do [contrato efetuado pela Câmara de Lagos](https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=10295389) no artigo 14º nrº 1 significa que para termos mais informações acerca do concurso ( quais as condições de elegibilidade ) temos de entrar em contato com o jurí do procedimento ?

-  [x] [Montijo](https://www.base.gov.pt/Base4/pt/detalhe/?type=entidades&id=304018) : mesmo contrato duplicado mas com preços contratuais diferentes

- [x] [IPO](https://www.base.gov.pt/Base4/pt/detalhe/?type=contratos&id=10295077) : uma das empresas apresentou uma proposta de 1 cêntimo - **Pode ser uma red flag**

- [x] Texto introdução tese
---

- [x] Atribuir cotação/peso a cada um dos parâmetros ( valor da flag e facilidade de implementação ) e criar uma coluna extra com uma média ponderada, por exemplo. Objetivo é atribuir um *score* para cada flag 

- [x] Instalar PostgreSQL num *Container* 
## Semana 4

6. Reunião 23/10/2023

- [x] Instalação PostgresSQL

7. Reunião 25/10/2023

- [x] Criar ficheiro com os passos de instalação do docker e postgres
- [x] Criar funções que permitam extrair informações de um contrato 
    - Exemplo : criar uma função cujo input seja o número de anúncio e retorne o preço base
- [x] Ao invés de utilizar um notebook, optar antes por um script *.py*
- [ ] Estudar OOP
- [ ] Possíveis bibliotecas a utilizar futuramente : Keras e Tensorflow 


## Semana 5

8. Reunião 30/10/2023

- [ ] Criar função para dar nomes de entidades adjudicatárias a partir do NIF
- [ ] Selecionar outras red flags

9. Reunião 01/11/2023
- Feriado

10. Reunião 03/11/2023

- Não acrescentei nada por causa do trabalho de STP 


## Semana 6

## Semana 7

11. Reunião 13/11/2023

- De entre os ajustes diretos, verificar para cada empresa o número de ajustes diretos efetuados, o número de ajustes diretos suspeitos e o rácio 

12. Reunião 15/11/2023

- Criar base de dados para guardar contratos celebrados entre diferentes NIFs. Ver quantos e quais contratos foram celebrados ( através do ID ) entre a empresa correspondente ao NIF1 e as empresas com NIF2 até NIFn. Fazer isso para todas as empresas. 




