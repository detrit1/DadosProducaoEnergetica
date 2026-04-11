# Análise de Produção de Petróleo com Python e MySQL

Este projeto realiza o processamento, limpeza, análise e armazenamento de dados de produção de petróleo a partir de arquivos CSV, utilizando Python, Pandas e MySQL.

---

## Funcionalidades

* Leitura de múltiplos arquivos CSV automaticamente
* Tratamento de dados inconsistentes

  * Remoção de BOM (`\ufeff`)
  * Padronização de colunas
  * Conversão de números no formato brasileiro (1.234,56 → 1234.56)
* Conversão para JSON
* Armazenamento em banco de dados MySQL
* Geração de visualizações com Pandas e Matplotlib

---

## Tecnologias utilizadas

* Python 3.x
* Pandas
* Matplotlib
* MySQL
* mysql-connector-python

---

## Estrutura do projeto

```
projeto
 ┣ dados/                  # arquivos CSV de entrada
 ┣ conversaoJSON.py       # script de conversão e limpeza
 ┣ dados_filtrados.json   # dados processados
 ┣ database.py            # inserção no MySQL
 ┣ analise.py             # geração de gráficos
 ┗ README.md
```

---

## Como executar

### 1. Clonar o repositório

```
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

---

### 2. Instalar as dependências

```
pip install pandas matplotlib mysql-connector-python
```

---

### 3. Executar o processamento dos dados

```
python conversaoJSON.py
```

Isso irá gerar o arquivo:

```
dados_filtrados.json
```

---

### 4. Configurar o banco de dados MySQL

No MySQL:

```
CREATE DATABASE producao_db;
```

---

### 5. Inserir os dados no banco

Edite as credenciais no arquivo `database.py`:

```
host="localhost"
user="root"
password="SUA_SENHA"
database="producao_db"
```

Depois execute:

```
python database.py
```

---

### 6. Executar análise e gráficos

```
python analise.py
```

---

## Exemplos de análises

* Produção por ano
* Distribuição por estado
* Bacias mais produtivas
* Instalações mais ativas
* Evolução temporal

---

## Desafios tratados

Durante o desenvolvimento, foram resolvidos problemas comuns de dados reais:

* Inconsistência nos nomes das colunas
* Encoding (UTF-8 com BOM)
* Dados numéricos armazenados como string
* Diferentes formatos de CSV

---

## Fonte dos dados

Os dados utilizados neste projeto foram obtidos a partir do portal oficial de dados abertos do governo brasileiro:

https://dados.gov.br/home

A plataforma reúne datasets públicos de diversas áreas e permite o uso livre dos dados, conforme suas diretrizes.

---

## Possíveis melhorias

* Desenvolvimento de dashboard interativo
* Criação de API REST
* Normalização do banco de dados
* Integração com ferramentas de Business Intelligence

---

## Autor

Pedro Stachuka

---

## Licença

Este projeto é de uso acadêmico e livre para estudos.
