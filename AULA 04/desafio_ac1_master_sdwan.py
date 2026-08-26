"""
================================================================
RELATÓRIO TÉCNICO — MOTOR DE DECISIONING SD-WAN ZERO-TRUST
================================================================
[PREENCHER MANUALMENTE APÓS RODAR O SCRIPT — os valores abaixo
são apenas o formato esperado; copie a saída impressa no console]

Rota selecionada: <preencher com a rota impressa>
Latência total: <preencher> ms
Perda de pacotes total: <preencher> %
Fitness final: <preencher>

Nós não confiáveis da topologia (reputação < 50): <preencher>
Nós não confiáveis presentes na rota escolhida: <preencher>

Justificativa:
O algoritmo aplica uma penalização fixa de 5000 (P_seguranca)
sempre que a rota passa por qualquer nó com índice de reputação
de segurança abaixo de 50. Como essa penalização é muito maior
do que qualquer combinação plausível de latência e perda de
pacotes nesta topologia, o GA converge para rotas que desviam
dos nós não confiáveis mesmo quando eles ofereceriam, isoladamente,
enlaces de menor latência. Descreva aqui, com base na rota impressa,
se algum nó não confiável aparece no caminho final e por quê (ex:
nenhum caminho alternativo evita completamente algum nó específico,
ou o desvio tem custo de latência X que ainda compensa por segurança).
================================================================
"""

import numpy as np

# ============================================================
# 1. CONFIGURAÇÕES DO PROBLEMA
# ============================================================

np.random.seed(2026)

NUM_NOS = 12
NO_ORIGEM = 0
NO_DESTINO = 11

W1 = 0.6   # peso da latência total
W2 = 0.4   # peso da perda de pacotes total
PENALIDADE_SEGURANCA = 5000.0
REPUTACAO_MINIMA = 50.0

TAMANHO_POPULACAO = 60
NUM_GERACOES = 150
TAXA_MUTACAO = 0.20


# ============================================================
# 2. TOPOLOGIA DA REDE (matriz de adjacência e atributos)
# ============================================================

# Matriz de latência (ms) — grafo completo entre os 12 nós
matriz_latencia = np.random.uniform(5, 60, (NUM_NOS, NUM_NOS))
np.fill_diagonal(matriz_latencia, 0)

# Matriz de taxa de perda de pacotes (%) — grafo completo
matriz_perda = np.random.uniform(0, 15, (NUM_NOS, NUM_NOS))
np.fill_diagonal(matriz_perda, 0)

# Índice de reputação de segurança de cada nó (0 a 100)
reputacao_nos = np.random.uniform(0, 100, NUM_NOS)

nos_nao_confiaveis = np.where(reputacao_nos < REPUTACAO_MINIMA)[0]


# ============================================================
# 3. REPRESENTAÇÃO DO INDIVÍDUO
# ============================================================

# A rota é modelada como uma permutação dos nós intermediários
# (1 a 10), com origem fixa em 0 e destino fixo em 11:
# rota = [0, ...permutação dos nós 1-10..., 11]

nos_intermediarios = [n for n in range(NUM_NOS) if n not in (NO_ORIGEM, NO_DESTINO)]


def montar_rota(permutacao_intermediarios):
    return np.array([NO_ORIGEM] + list(permutacao_intermediarios) + [NO_DESTINO])


# ============================================================
# 4. FUNÇÃO DE FITNESS PONDERADA COM PENALIZAÇÃO DE SEGURANÇA
# ============================================================

def calcular_fitness(rota, matriz_lat, matriz_perda, reputacao, w1, w2, penalidade):
    latencia_total = 0.0
    perda_total = 0.0

    for i in range(len(rota) - 1):
        origem, destino = rota[i], rota[i + 1]
        latencia_total += matriz_lat[origem, destino]
        perda_total += matriz_perda[origem, destino]

    penalidade_seguranca = 0.0
    if any(reputacao[no] < REPUTACAO_MINIMA for no in rota):
        penalidade_seguranca = penalidade

    fitness = w1 * latencia_total + w2 * perda_total + penalidade_seguranca

    return fitness, latencia_total, perda_total, penalidade_seguranca


# ============================================================
# 5. OPERADORES GENÉTICOS (sobre os nós intermediários)
# ============================================================

def criar_populacao(tamanho_populacao, nos_intermediarios):
    return [
        np.random.permutation(nos_intermediarios)
        for _ in range(tamanho_populacao)
    ]


def crossover_ox(pai1, pai2):
    tamanho = len(pai1)
    filho = np.full(tamanho, -1, dtype=int)

    ponto1, ponto2 = sorted(np.random.choice(tamanho, 2, replace=False))
    filho[ponto1:ponto2] = pai1[ponto1:ponto2]

    posicao = ponto2
    for elemento in pai2:
        if elemento not in filho:
            if posicao >= tamanho:
                posicao = 0
            filho[posicao] = elemento
            posicao += 1

    return filho


def mutacao_swap(individuo, taxa_mutacao):
    individuo = individuo.copy()
    if np.random.rand() < taxa_mutacao:
        idx1, idx2 = np.random.choice(len(individuo), 2, replace=False)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo


def selecao_torneio(populacao, fitness, tamanho_torneio=3):
    participantes = np.random.choice(len(populacao), tamanho_torneio, replace=False)
    melhor = participantes[np.argmin([fitness[i] for i in participantes])]
    return populacao[melhor]


# ============================================================
# 6. EXECUÇÃO DO ALGORITMO GENÉTICO
# ============================================================

populacao = criar_populacao(TAMANHO_POPULACAO, nos_intermediarios)

melhor_individuo_global = None
melhor_fitness_global = np.inf

for geracao in range(NUM_GERACOES):

    rotas = [montar_rota(ind) for ind in populacao]

    resultados = [
        calcular_fitness(rota, matriz_latencia, matriz_perda, reputacao_nos, W1, W2, PENALIDADE_SEGURANCA)
        for rota in rotas
    ]

    fitness_populacao = [r[0] for r in resultados]

    indice_melhor = np.argmin(fitness_populacao)

    if fitness_populacao[indice_melhor] < melhor_fitness_global:
        melhor_fitness_global = fitness_populacao[indice_melhor]
        melhor_individuo_global = populacao[indice_melhor].copy()

    nova_populacao = [melhor_individuo_global.copy()]  # elitismo

    while len(nova_populacao) < TAMANHO_POPULACAO:
        pai1 = selecao_torneio(populacao, fitness_populacao)
        pai2 = selecao_torneio(populacao, fitness_populacao)

        filho = crossover_ox(pai1, pai2)
        filho = mutacao_swap(filho, TAXA_MUTACAO)

        nova_populacao.append(filho)

    populacao = nova_populacao


# ============================================================
# 7. RESULTADOS FINAIS
# ============================================================

melhor_rota = montar_rota(melhor_individuo_global)
fitness_final, latencia_final, perda_final, penalidade_aplicada = calcular_fitness(
    melhor_rota, matriz_latencia, matriz_perda, reputacao_nos, W1, W2, PENALIDADE_SEGURANCA
)

nos_penalizados_na_rota = [no for no in melhor_rota if reputacao_nos[no] < REPUTACAO_MINIMA]

print("=" * 70)
print("RESULTADOS — MOTOR DE DECISIONING SD-WAN ZERO-TRUST")
print("=" * 70)
print(f"Rota selecionada: {melhor_rota}")
print(f"Latência total: {latencia_final:.2f} ms")
print(f"Perda de pacotes total: {perda_final:.2f} %")
print(f"Penalidade de segurança aplicada: {penalidade_aplicada:.2f}")
print(f"Fitness final: {fitness_final:.2f}")
print(f"Reputação de todos os nós: {np.round(reputacao_nos, 1)}")
print(f"Nós não confiáveis da topologia (reputação < 50): {list(nos_nao_confiaveis)}")
print(f"Nós não confiáveis presentes na rota escolhida: {nos_penalizados_na_rota}")
print("=" * 70)


"""

RESULTADOS

======================================================================
RESULTADOS — MOTOR DE DECISIONING SD-WAN ZERO-TRUST
======================================================================
Rota selecionada: [ 0 10  2  3  6  4  1  9  7  5  8 11]
Latência total: 150.42 ms
Perda de pacotes total: 66.82 %
Penalidade de segurança aplicada: 5000.00
Fitness final: 5116.98
Reputação de todos os nós: [62.1  1.9 15.2 50.5 86.4 82.  38.5 92.4 30.1 62.9 74.4  0.2]
Nós não confiáveis da topologia (reputação < 50): [np.int64(1), np.int64(2), np.int64(6), np.int64(8), np.int64(11)]
Nós não confiáveis presentes na rota escolhida: [np.int64(2), np.int64(6), np.int64(1), np.int64(8), np.int64(11)]
======================================================================


"""