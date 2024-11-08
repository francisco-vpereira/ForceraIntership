# Instalação Docker e PostgreSQL

1. Fazer download do *docker* : `sudo pacman -S docker` para distribuições Arch-based 

2. Fazer pull da imagem do Postgres : `docker pull postgres`. Se não funcionar e der *permission denied* pode-se usar `sudo docker pull postgres` ou então consultar o ponto 8.

3. Para iniciar o container do Postgres :  

``` 
docker run --name postgres -p 5434:5432 -e POSTGRES_USER=aim4ps -e POSTGRES_PASSWORD=aim4ps -d postgres
```

em que,

* --name : nome do container

* -p : mapeamento das portas para aceder à BD fora do container (ex: python). Neste caso, de fora acedemos pelo 5434, dentro do container pelo 5432

* -e : passar variáveis de ambiente. Neste caso passamos o user e o password a ser usado para "instalar" o postgres no docker


4. Para criar as tabelas na BD corremos este comando no mesmo diretório onde está o ficheiro *dump2.sql* :

    ``` cat dump2.sql | docker exec -i postgres psql -U aim4ps -d postgres ```

em que ,
* dump2.sql : ficheiro com o script
* -U : user definido no comando anterior



5. Foi preciso criar um user na BD
    1. `- docker exec -it postgres bash` : para aceder ao container a partir do terminal. `docker exec -it /bin/bash` também funciona acho eu
  
    2. `psql -h localhost -p 5432 -U aim4ps` : acedemos ao PostgreSQL
  
    3. ```
       CREATE USER myuser WITH PASSWORD '1234';
       \c aim4ps
       GRANT ALL PRIVILEGES ON ALL TABLES    IN SCHEMA public to myuser 
       GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to myuser
       GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public to myuser
       GRANT ALL PRIVILEGES ON DATABASE aim4ps TO myuser;
       \q
       exit
       ```
       para criar um user chamado *myuser*. 

6. Para parar e iniciar o container, sem ter que criar de novo, é só correr : 
    ``` 
    docker stop postgres
    docker start postgres
    ```
7. Para ver o estado de um container corremos : `docker ps` e vemos a coluna STATUS


8. Quando o docker dá erro de *permission denied* passa a funcionar ao executar os seguintes comandos: 
    ```
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
    $ newgrp docker   
    ```
<br> 

<br>

***

# Ligação ao Python

***

9. Para ligar o Postgres ao Python precisamos de instalar o package *psycopg2*

    ```
    pip install --upgrade pip
    pip install psycopg2
    ```


10. Dentro de um ficheiro python :

    1. Criar a ligação com o Postgres
    
    ```
    # Esta é uma possibilidade
    conn = psycopg2.connect(
                    host="localhost",
                    port = 5434,
                    database="aim4ps",
                    user= "myuser",
                    password="1234")
    ```

    2. Criar  a cursor : `cur = conn.cursor()`
    
    3. Executar um statement qualquer ( neste caso : imprimir o nome das colunas da tabela *CONTRACTS* ) : 
        
    ```
    cur.execute('''
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'CONTRACTS'; ''')

    cur.fetchall()
    ```






