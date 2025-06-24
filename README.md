# 📘 Análise de Propriedade de Código em Sistemas Embarcados com RTOS FLOSS

**Disciplina:** Software Embarcado  
**Aluno:** Janei Vieira  
**Professor:** [Nome do Professor]  
**Projeto Analisado:** Zephyr RTOS  
**Data:** [Data da Entrega]

---

## 1. Introdução

A sustentabilidade de sistemas embarcados baseados em RTOS FLOSS (Free/Libre and Open Source Software) depende não apenas de sua arquitetura, mas também da forma como seu código é mantido e distribuído entre os colaboradores. Este relatório apresenta uma análise da modularidade e da propriedade coletiva do código no projeto **Zephyr RTOS**, utilizando heurísticas baseadas em commits, Degree of Authorship (DOA) e Truck Factor (TF).

---

## 2. Fundamentação Teórica

### 2.1 Modularidade de Código

A modularidade representa a capacidade de um sistema ser dividido em partes independentes e reutilizáveis. Em um RTOS, essa prática contribui para a manutenibilidade e escalabilidade do sistema.

### 2.2 Propriedade Coletiva de Código

A propriedade coletiva é um princípio no qual qualquer desenvolvedor pode modificar qualquer parte do código, promovendo colaboração e resiliência na equipe.

### 2.3 Heurísticas Baseadas em Commits

São métodos para rastrear o histórico de alterações no código, permitindo identificar autores dominantes e áreas críticas com pouca revisão ou contribuição.

### 2.4 Degree of Authorship (DOA)

O DOA quantifica o domínio de um desenvolvedor sobre um arquivo, considerando o commit original e alterações subsequentes.

### 2.5 Truck Factor (TF)

O TF estima quantos desenvolvedores precisam sair do projeto para que ele se torne insustentável. Quanto menor o TF, maior o risco.

---

## 3. Metodologia

### 3.1 Projeto Escolhido

Foi escolhido o projeto **Zephyr RTOS**, disponível no repositório oficial: [https://github.com/zephyrproject-rtos/zephyr](https://github.com/zephyrproject-rtos/zephyr)

### 3.2 Ferramentas Utilizadas

- **PyDriller**: para análise do histórico Git.
- **Python (Pandas/Matplotlib)**: para manipulação e visualização de dados.
- **git-truck** *(opcional)*: para estimar o Truck Factor.

### 3.3 Escopo da Análise

Foram analisados os arquivos `.c` e `.cpp` nos diretórios `kernel/` e `arch/`, correspondentes ao núcleo do RTOS.

---

## 4. Resultados

### 4.1 Desenvolvedores Mais Ativos por Módulo

```text
(Exemplo de tabela extraída do script)
| Desenvolvedor     | Commits no núcleo | Módulos mais atuantes        |
|-------------------|-------------------|-------------------------------|
| John Doe          | 152               | kernel/, arch/x86/            |
| Jane Smith        | 97                | kernel/sched.c, init.c        |
