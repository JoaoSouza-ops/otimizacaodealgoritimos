import numpy as np
np.random.seed(42)

# Problema da Mochila (Blindagem de Ativos)
weights = np.array([12, 2, 1, 4, 1])   # Custo/Consumo de Memória dos ativos
values = np.array([4, 2, 1, 10, 2])    # Cobertura de Risco/Valor do ativo
max_weight = 15

pop_size = 10
num_genes = len(weights)
generations = 10
mutation_rate = 0.1

# Inicialização da População (Matriz Binária 10x5)
population = np.random.randint(0, 2, size=(pop_size, num_genes))


def calculate_fitness(ind):
    total_weight = np.sum(ind * weights)
    total_value = np.sum(ind * values)
    # TODO 1: restrição de peso -- penaliza com fitness=0 se estourar a capacidade
    if total_weight > max_weight:
        return 0
    return total_value


def tournament_selection(pop, fitnesses):
    # TODO 2: seleção por torneio -- escolhe 2 indivíduos aleatórios e retorna o melhor
    idx1, idx2 = np.random.randint(0, len(pop), size=2)
    if fitnesses[idx1] >= fitnesses[idx2]:
        return pop[idx1].copy()
    else:
        return pop[idx2].copy()


def crossover(parent1, parent2):
    point = np.random.randint(1, num_genes)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2


def mutate(ind):
    for i in range(num_genes):
        if np.random.rand() < mutation_rate:
            ind[i] = 1 - ind[i]
    return ind


melhor_fitness_por_geracao = []
melhor_individuo_global = None
melhor_fitness_global = -1

# Loop Evolutivo
for g in range(generations):
    fitnesses = np.array([calculate_fitness(ind) for ind in population])

    # Acompanha o melhor indivíduo da geração/execução
    idx_melhor = np.argmax(fitnesses)
    if fitnesses[idx_melhor] > melhor_fitness_global:
        melhor_fitness_global = fitnesses[idx_melhor]
        melhor_individuo_global = population[idx_melhor].copy()
    melhor_fitness_por_geracao.append(fitnesses.max())

    new_population = []
    for _ in range(pop_size // 2):
        p1 = tournament_selection(population, fitnesses)
        p2 = tournament_selection(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        new_population.extend([mutate(c1), mutate(c2)])

    population = np.array(new_population)

print("[LAB 02] Execução completa")
print("Melhor fitness por geração:", melhor_fitness_por_geracao)
print("Melhor indivíduo encontrado:", melhor_individuo_global)
print("Peso total:", np.sum(melhor_individuo_global * weights))
print("Valor total (fitness):", melhor_fitness_global)
