# Escrever números aleatórios num ficheiro .txt todos os minutos


### 1. Criar ficheiro .txt 

``` 
$ touch /PATH_TO_FILE/random_number.txt
```

### 2. Inserir manualmente números aleatórios em *random_number.txt*

```
$ echo $RANDOM >> /PATH_TO_FILE/random_number.txt
```

### 3. Definir cronjob

```
$ crontab -e


* * * * * /usr/bin/zsh -c 'echo $RANDOM >> /PATH_TO_FILE/random_number.txt'
```

### 4. Visualização 

```
$ crontab -l  # Para ver lista de cron jobs

$ watch cat /PATH_TO_FILE/random_number.txt   # Para ver update em tempo real ao ficheiro
```
