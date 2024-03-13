# Passos para correr script na AWS

Nomes dos ficheiros : 

- process_update.py

- none_cases.py

- flag_calculator.py

- table_update.py

Localização do ficheiro : 

```/home/francisco/MECAD/2º Ano/Estágio/RepoForcera/scripts/cron_jobs/final_scripts_v2 ```


Observação : 
    
- Diretório está sincronizado com o github
    
- Já foi criada função **lamda_handler(event, context)** dentro do script principal 

#### 1. Criar ficheiro chamado *dockerfile* e guardar no mesmo diretório do script principal


```
FROM public.ecr.aws/lambda/python:3.12

RUN pip3 install requests psycopg2-binary

COPY process_update.py ${LAMBDA_TASK_ROOT}
COPY flag_calculator.py ${LAMBDA_TASK_ROOT}
COPY table_update.py ${LAMBDA_TASK_ROOT}
COPY none_cases.py ${LAMBDA_TASK_ROOT}

CMD [ "process_update.lambda_handler" ]
```

#### 2. Lambda Function : Criar função Lambda

- Ao criar a função escolher opção **Container image**

#### 3. IAM : Criar User

- Selecionar **Users**

- Criar novo user

- Guardar ID e Password ( não voltam a ser disponibilizados )


#### 4. Amazon ECR : criar repositório na AWS

- Criar um repositório onde irá ser armazenado o container

- Selecionar o repositório

- Selecionar **View push commands**

- Aceder ao diretório onde está armazenado o script principal

- Correr comandos da secção 4.3
 
- Fazer refresh da página **Amazon ECR > Private registry > Repositories > NOME_REPOSITORIO**. Se os comandos correrem corretamente, a coluna **Pushed at** tem a data em que foram feitas as alterações ao repositório

- Clicar em *latest* em **Image tag**. Copiar código **URI**


#### 5. Lambda Function : Deploy new image

- Clicar em **Deploy new image**

- Copiar código do ponto 4.7 na entrada *Docker container image from selectecd repository* e guardar

- Testar


#### 6. Automatizar processo

- Criar diretório **.github/workflow**

- Pode ser preciso atualizar o token OU editar e dar premissão para, ao dar push, permitir criar este novo diretório

- Criar ficheiro **container.yml** dentro do diretório **workflow**

```
name: Push to AWS ECR

on:
  push:
    branches: [master]

jobs:
    push-ids_collector:
        runs-on: ubuntu-latest
    
        steps:
          - name: Checkout
            uses: actions/checkout@v2
            
          - name: Set up Docker Buildx
            uses: docker/setup-buildx-action@v2

          - name: AWS Configure CLI
            uses: aws-actions/configure-aws-credentials@v1
            with:
              aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
              aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
              aws-region: eu-north-1
          # Cuidado com a região na linha acima
          # AWS_ACESS_KEY_ID e AWS_SECRET_ACESS_KEY são os dados guardados ao criar o user
          # Têm que ser guardados no github. Settings > Secrets and variables > Actions


          - name: Login to Amazon ECR
            id: login-ecr
            uses: aws-actions/amazon-ecr-login@v1

        
          - name: Build, tag, and push docker image to Amazon ECR
            env:
              REGISTRY: ${{ steps.login-ecr.outputs.registry }}
              REPOSITORY: container_flags
              IMAGE_TAG: latest
              # Cuidado com o nome do repositório. Tem de coincidir com o que foi criado no ECR
            

            # Estes são os comandos em **View push commands** do repositório
            run: |
              docker build -t container_flags ./scripts/cron_jobs/final_scripts_v2/
              docker tag container_flags:latest 654654334568.dkr.ecr.eu-north-1.amazonaws.com/container_flags:latest
              docker push 654654334568.dkr.ecr.eu-north-1.amazonaws.com/container_flags:latest

```

Sempre que se fizerem alterações ao código e se der push para o github, o repositório da AWS irá ser atualizado. 


- Criação de um Schedule : **Amazon EventBridge**

- Em **Cloud Watch** podemos ver o estado do processo

- Na secção Actions, no repositório do github, podemos ver se existem erros ao sincronizar o repositório do github com o da AWS





