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
