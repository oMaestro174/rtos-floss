import argparse
from pydriller import Repository
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import islice

parser = argparse.ArgumentParser(description="Análise rápida de autoria no Zephyr RTOS")
parser.add_argument('--repo', required=True, help="Caminho local do repositório Zephyr")
parser.add_argument('--commits', type=int, default=500, help="Limite de commits (ex: 500)")
args = parser.parse_args()

REPO_PATH = args.repo
COMMIT_LIMITE = args.commits

DIRS_INTERESSE = ['kernel/']
EXTENSOES = ('.c', '.cpp')
dados = defaultdict(lambda: defaultdict(int))
original_author = {}
modificacoes_outros = defaultdict(int)

print("🔍 Analisando repositório:", REPO_PATH)
repo_iter = Repository(REPO_PATH).traverse_commits()
for commit in islice(repo_iter, COMMIT_LIMITE):
    autor = commit.author.name
    for arquivo in commit.modified_files:
        caminho = arquivo.new_path
        if not caminho:
            continue
        if caminho.endswith(EXTENSOES) and any(caminho.startswith(d) for d in DIRS_INTERESSE):
            if caminho not in original_author:
                original_author[caminho] = autor
            if autor != original_author[caminho]:
                modificacoes_outros[caminho] += 1
            dados[caminho][autor] += 1

doa_resultado = []
for arquivo, autores in dados.items():
    penalidade = 0.1 * modificacoes_outros[arquivo]
    for autor, n_commits in autores.items():
        doa = (1.0 if autor == original_author[arquivo] else 0.0)
        doa += 0.5 * n_commits
        doa -= penalidade
        doa_resultado.append({
            'arquivo': arquivo,
            'autor': autor,
            'commits': n_commits,
            'doa': round(doa, 2)
        })

df_doa = pd.DataFrame(doa_resultado)

print("\n📊 Top 5 autores por DOA:")
print(df_doa.groupby('autor')['doa'].sum().sort_values(ascending=False).head(5))

plt.figure(figsize=(10, 4))
df_doa.groupby('autor')['commits'].sum().sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Desenvolvedores (Últimos Commits)')
plt.ylabel('Commits')
plt.xlabel('Autor')
plt.tight_layout()
plt.savefig("grafico_commits_autores.png")
plt.close()

plt.figure(figsize=(12, 6))
df_doa.groupby('arquivo')['doa'].max().sort_values(ascending=False).head(10).plot(kind='barh', color='lightgreen')
plt.title('Arquivos com Maior DOA')
plt.xlabel('DOA')
plt.tight_layout()
plt.savefig("grafico_doa_arquivos.png")
plt.close()

# Gerar tabela resumo
resumo = []
for autor in df_doa['autor'].unique():
    df_autor = df_doa[df_doa['autor'] == autor]
    commits_total = df_autor['commits'].sum()
    # Top 2 módulos/arquivos mais atuantes
    mais_atuantes = (
        df_autor.groupby('arquivo')['commits']
        .sum()
        .sort_values(ascending=False)
        .head(2)
        .index.tolist()
    )
    resumo.append({
        'Desenvolvedor': autor,
        'Commits no núcleo': commits_total,
        'Módulos mais atuantes': ', '.join(mais_atuantes)
    })

df_resumo = pd.DataFrame(resumo)
df_resumo = df_resumo.sort_values('Commits no núcleo', ascending=False).head(10)

print("\n| Desenvolvedor     | Commits no núcleo | Módulos mais atuantes        |")
print("|-------------------|-------------------|-------------------------------|")
for _, row in df_resumo.iterrows():
    print(f"| {row['Desenvolvedor']:<18} | {row['Commits no núcleo']:<17} | {row['Módulos mais atuantes']:<30} |")

print("\n✅ Análise concluída.")
print(" - grafico_commits_autores.png")
print(" - grafico_doa_arquivos.png")
