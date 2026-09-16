import numpy as np
np.random.seed(42)


def fitness_function(position):
    return np.sum(position**2)


num_particles = 10
dimensions = 2
max_iter = 15

X = np.random.uniform(-5, 5, (num_particles, dimensions))
V = np.random.uniform(-1, 1, (num_particles, dimensions))

pbest_X = np.copy(X)
pbest_fitness = np.array([fitness_function(p) for p in pbest_X])

gbest_index = np.argmin(pbest_fitness)
gbest_X = np.copy(pbest_X[gbest_index])

w = 0.5
c1 = 1.5
c2 = 1.5

historico_gbest = []

for t in range(max_iter):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()

        # Equação de atualização da velocidade da partícula i
        V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))

        X[i] = X[i] + V[i]

        current_fitness = fitness_function(X[i])
        if current_fitness < pbest_fitness[i]:
            pbest_fitness[i] = current_fitness
            pbest_X[i] = X[i]

            if current_fitness < fitness_function(gbest_X):
                gbest_X = X[i].copy()  # CORRIGIDO: sem .copy() o gbest_X ficava "grudado"
                                        # na mesma memória da partícula, mudando sozinho depois

    historico_gbest.append(fitness_function(gbest_X))

print(f"[LAB 03] Melhor posição encontrada pelo Enxame (gbest): {gbest_X}")
print(f"[LAB 03] Fitness do gbest: {fitness_function(gbest_X):.6f}")
print(f"[LAB 03] Histórico do fitness do gbest por iteração: {[round(v,4) for v in historico_gbest]}")
