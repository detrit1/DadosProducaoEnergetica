import pandas as pd
import matplotlib.pyplot as plt

# carregar dados
df = pd.read_json("dados_filtrados.json")

# garantir que ano seja numérico
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
df["oleo"] = pd.to_numeric(df["oleo"], errors="coerce")

print("\nEstatísticas de óleo por ano (média, máximo, mínimo):")
print(df.groupby("ano")["oleo"].agg(["mean", "max", "min"]).round(2))

if "estado" in df.columns:
    print("\nEstatísticas de óleo por estado (média, máximo, mínimo):")
    print(df.groupby("estado")["oleo"].agg(["mean", "max", "min"]).round(2))

if "bacia" in df.columns:
    print("\nEstatísticas de óleo por bacia (média, máximo, mínimo):")
    print(df.groupby("bacia")["oleo"].agg(["mean", "max", "min"]).round(2))

df.groupby("ano").size().plot(kind="bar")
plt.title("Registros por Ano")
plt.xlabel("Ano")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
plt.show()

if "estado" in df.columns:
    df["estado"].value_counts().plot(kind="bar")
    plt.title("Distribuição por Estado")
    plt.xlabel("Estado")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45)
    plt.show()
else:
    print("⚠️ Coluna 'estado' não está no JSON")

df["bacia"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Bacias")
plt.xlabel("Bacia")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
plt.show()

df["instalacao"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Instalações")
plt.xlabel("Instalação")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
plt.show()

df.groupby("ano").size().plot(kind="line")
plt.title("Evolução Temporal")
plt.xlabel("Ano")
plt.ylabel("Quantidade de Registros")
plt.xticks(rotation=45)
plt.show()