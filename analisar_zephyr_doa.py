from pydriller import Repository
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Caminho ou URL do repositório
REPO_URL = "https://github.com/zephyrproject-rtos/zephyr"

# Filtros por diretório e extensão
DIRS_INTERESSE = ['kernel/', 'arch/']
EXTENSOES = ('.c', '.cpp')

# Armazenamento de dados
dados = defaultdict(lambda: defaultdict(int))  # dados[arquivo][autor]
original_author = {}  # dados[arquivo] = autor original
modificacoes_outros = defaultdict(int)

print("🔍 Analisando commits...")

for commit in Repository(REPO_URL).traverse_commits():
    autor = commit.author.name

    for arquivo in commit.modified_files:
        caminho = arquivo.new_path
        if not caminho:
            continue

        if caminho.endswith(EXTENSOES) and any(d in caminho for d in DIRS_INTERESSE):
            if caminho not in original_author:
                original_author[caminho] = autor
            if autor != original_author[caminho]:
                modificacoes_outros[caminho] += 1
            dados[caminho][autor] += 1

# Cálculo do DOA simplificado
doa_resultado = []

for arquivo, autores in dados.items():
    for autor, n_commits in autores.items():
        doa = (1.0 if autor == original_author[arquivo] else 0.0)
        doa += 0.5 * n_commits
        doa -= 0.1 * modificacoes_outros[arquivo]
        doa_resultado.append({
            'arquivo': arquivo,
            'autor': autor,
            'commits': n_commits,
            'doa': round(doa, 2)
        })

df_doa = pd.DataFrame(doa_resultado)

# 🔝 Top 10 autores por DOA
print("\n📊 Top 10 autores por DOA:")
print(df_doa.groupby('autor')['doa'].sum().sort_values(ascending=False).head(10))

# 📈 Gráfico de commits por autor
plt.figure(figsize=(10, 5))
df_doa.groupby('autor')['commits'].sum().sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Desenvolvedores - Commits nos arquivos núcleo')
plt.ylabel('Commits')
plt.xlabel('Autor')
plt.tight_layout()
plt.savefig("grafico_commits_autores.png")
plt.close()

# 📈 Gráfico de DOA por arquivo
plt.figure(figsize=(12, 6))
df_doa.groupby('arquivo')['doa'].max().sort_values(ascending=False).head(15).plot(kind='barh', color='salmon')
plt.title('Arquivos com maior grau de autoria (DOA)')
plt.xlabel('DOA')
plt.tight_layout()
plt.savefig("grafico_doa_arquivos.png")
plt.close()

print("\n✅ Análise concluída. Gráficos salvos:")
print(" - grafico_commits_autores.png")
print(" - grafico_doa_arquivos.png")
