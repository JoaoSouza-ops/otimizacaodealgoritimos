import numpy as np
np.random.seed(42)


def rastrigin(x):
    return 10 * len(x) + sum(x**2 - 10 * np.cos(2 * np.pi * x))


def local_search_hill_climbing(solution, step_size=0.01, max_steps=20):
    """Mecanismo de Intensificação (Aprendizado Individual / Memética)"""
    current_sol = np.copy(solution)
    current_fit = rastrigin(current_sol)

    for _ in range(max_steps):
        # Gera um vizinho adicionando ruído aleatório
        neighbor = current_sol + np.random.uniform(-step_size, step_size, size=len(solution))
        neighbor_fit = rastrigin(neighbor)

        # Se o vizinho for melhor (menor fitness), aceita a nova solução
        if neighbor_fit < current_fit:
            current_sol, current_fit = neighbor, neighbor_fit

    return current_sol, current_fit


initial_solution = np.array([2.5, -3.1])
refined_solution, final_fit = local_search_hill_climbing(initial_solution)

print(f"[LAB 05] Solução Inicial: {initial_solution} | Fitness: {rastrigin(initial_solution):.4f}")
print(f"[LAB 05] Solução Refinada: {refined_solution} | Fitness: {final_fit:.4f}")

# Executando várias vezes para ver a variabilidade do hill climbing puramente local
print("\n[LAB 05] Repetindo 5 vezes para observar a variabilidade (step_size=0.01, max_steps=20):")
for i in range(5):
    refined, fit = local_search_hill_climbing(initial_solution)
    print(f"  Execução {i+1}: fitness final = {fit:.4f}")
