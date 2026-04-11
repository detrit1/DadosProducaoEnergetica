# Analise de Producao de Petroleo

Este projeto processa arquivos CSV de producao energetica, gera JSON consolidado, calcula estatisticas e pode carregar dados no MySQL.

## Funcionalidades

- Leitura automatica de varios CSVs da pasta `dados/`
- Tratamento de colunas e normalizacao de valores numericos
- Conversao para JSON consolidado
- Calculo de media, maximo e minimo da producao de oleo
- Geracao opcional de graficos PNG
- Carga opcional para MySQL

## Script unico (pipeline)

O fluxo completo foi centralizado em [pipeline.py](pipeline.py).

### Dependencias

```bash
pip install pandas matplotlib mysql-connector-python
```

### Execucao basica

```bash
python3 pipeline.py
```

Saidas principais:

- `dados_filtrados.json`
- Estatisticas no terminal (por ano, estado e bacia)

### Gerar graficos

```bash
python3 pipeline.py --plots
```

Saida adicional:

- Pasta `graficos/` com arquivos PNG

### Carregar no MySQL

```bash
python3 pipeline.py --mysql
```

Variaveis de ambiente opcionais para conexao:

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=SUA_SENHA
export DB_NAME=producao_db
```

### Execucao completa

```bash
python3 pipeline.py --plots --mysql
```

## Estrutura do projeto

```text
DadosProducaoEnergetica/
  dados/
  pipeline.py
  conversaoJSON.py
  graph.py
  DataBank.py
  insertJsonData.py
  testData.py
  dados_filtrados.json
  README.md
```

## Fonte dos dados

Dados publicos obtidos em:

https://dados.gov.br/home
