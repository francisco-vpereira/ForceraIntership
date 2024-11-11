# Estrutura do diretório / *Folder Structure*


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

*Directory containing Python scripts and a Dockerfile for deployment on AWS. These are the same scripts found in `cron_jobs/final_scripts`, except for the part where environment variables are defined to access the database.*

***

#### 2. Plot_datasets

*Csv files, extracted from the database, to create plots.*

#### 3. PostgreSQL

*Set of PostgreSQL queries developed in order to implement the different flags constructed during this internship + create auxiliary tables.*

#### 4. cron_jobs

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


<br>

*Directory containing the automated process for calculating flags and updating the final table in PostgreSQL.*

*The final product is in the **final_scripts** directory. In **flag_calculator.py**, all functions for calculating the different identifiers/flags are defined. In **table_update.py**, an auxiliary table in the database is populated, which is used to calculate indicators in **flag_calculator.py**. In **none_cases.py**, a prevention mechanism is developed to handle cases where the script may not run as expected. The final script is **process_update.py**.*

*The process is described in detail in the README file.*

***


#### 3. scripts_py

```
scripts_py
├── flags.py
├── functions.py
└── script.py
```

Versão preliminar do produto final. Script **functions.py** contém funções auxiliares para extrair informação da tabela principal da base de dados. 

*Preliminary version of the final product. The **functions.py** script contains helper functions to extract information from the main table in the database.*


