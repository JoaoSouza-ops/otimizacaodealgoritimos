import numpy as np

# Grafo de Latência entre Roteadores (Matriz de Custo)
latency_matrix = np.array([
    [0, 5, 2, 9],
    [5, 0, 3, 1],
    [2, 3, 0, 7],
    [9, 1, 7, 0]
])

num_nodes = len(latency_matrix)
pheromone = np.ones((num_nodes, num_nodes))
rho = 0.25


def update_pheromone(pheromone_matrix, paths, costs, rho):
    # TODO 1: evaporação em toda a matriz
    pheromone_matrix = (1 - rho) * pheromone_matrix

    # TODO 2: depósito de feromônio para cada caminho percorrido
    for path, cost in zip(paths, costs):
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            pheromone_matrix[u][v] += (1.0 / cost)

    return pheromone_matrix


mock_paths = [[0, 2, 1, 3], [0, 1, 3]]
mock_costs = [6.0, 6.0]

updated_pheromone = update_pheromone(pheromone, mock_paths, mock_costs, rho)
print("[LAB 04] Matriz de Feromônio Atualizada:\n", updated_pheromone)

# Atratividade inicial (eta) de cada enlace: eta = 1 / latência
print("\n[LAB 04] Atratividade inicial (eta = 1/latência) por enlace:")
with np.errstate(divide='ignore'):
    eta = np.where(latency_matrix > 0, 1.0 / latency_matrix, 0)
print(np.round(eta, 4))
