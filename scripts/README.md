# Estrutura do diretório


#### 1. **AWS**
```
AWS
├── dockerfile
├── flag_calculator.py
├── none_cases.py
├── process_update.py
└── table_update.py
```
Diretório que contém scripts em python e ficheiro dockerfile a fim de fazer deploy na AWS. São exatamente os mesmos scripts contidos em `cron_jobs/final_scripts`, exceto na parte onde são definidas as variáveis ambientes a fim de aceder à base de dados. 

*Directory containing Python scripts and a Dockerfile for deployment on AWS. These are the same scripts found in cron_jobs/final_scripts, except for the part where environment variables are defined to access the database.*

***

#### 2. cron_jobs

```
cron_jobs
├── README.md
├── final_scripts
│   ├── flag_calculator.py
│   ├── none_cases.py
│   ├── process_update.py
│   └── table_update.py
└── first_approach
    ├── daily_flags.py
    ├── daily_ids.py
    ├── flags_calculator.py
    ├── r017.py
    └── r019.py
```
Diretório que contém o processo de automação de cálculo de flags e update da tabela final em PostgreSQL.

O produto final está no diretório **final_scripts**. Em **flag_calculator.py** são definidas todas as funções que calculam os diferentes identificadores/flags desenvolvidos. Em **table_update.py** é preenchida uma tabela auxiliar presente na base de dados que é utilizada para calcular os indicadores em **flag_calculator.py**. Em **none_cases.py** é desenvolvido um mecanismo de prevenção na eventualidade de o script não correr como é suposto. O script final é **process_update.py**. 
O processo está descrito detalhadamente no ficheiro README. 

***

#### 3. notebooks

```
notebooks
├── 1. análise_inicial
│   ├── contratos.ipynb
│   ├── contratospublicos.ipynb
│   ├── contratos_v2.ipynb
│   └── flags.ipynb
├── 2. análise_intermedia
│   ├── contratospublicos.ipynb
│   ├── contratos_v2.ipynb
│   ├── R018_NEC.ipynb
│   ├── R049_adaptado.ipynb
│   ├── R049.ipynb
│   └── R059.ipynb
└── 3. análise_final
    ├── automacao.ipynb
    ├── flagR017.ipynb
    ├── flagR019.ipynb
    ├── Plots.ipynb
    ├── precoscontr_analise.ipynb
    ├── r018.py
    ├── r019.py
    ├── R031.ipynb
    ├── R051_HHI.ipynb
    ├── R051.ipynb
    ├── R051_variante.ipynb
    └── teste.py
```
Processo de análise e construção das flags foi feito maioritarimente em Jupyter Notebook. 


***

#### 4. scripts_py

```
scripts_py
├── flags.py
├── functions.py
└── script.py
```

Versão preliminar do produto final. Script **functions.py** contém funções auxiliares para extrair informação da tabela principal da base de dados. 

#### 5. AWS_step
Descrição do procedimento para pôr o código a correr nunma função Lambda diariamente. 


