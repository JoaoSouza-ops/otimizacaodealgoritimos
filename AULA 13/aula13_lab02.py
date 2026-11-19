import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize

class KubernetesClusterProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Replicas da API (2 a 40), x2: Worker Nodes (1 a 12)
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([2, 1]),
            xu=np.array([40, 12]),
            vtype=int
        )

    def _evaluate(self, x, out, *args, **kwargs):
        replicas, nodes = x[0], x[1]

        # TODO 1: Calcule o Tempo de Resposta (ms): (600 / replicas) + (200 / nodes)
        f1_tempo = (600/replicas) + (200/nodes)

        # TODO 2: Calcule o Custo Mensal (USD): (replicas * 12) + (nodes * 85)
        f2_custo = (replicas * 12) + (nodes * 85)

        out["F"] = [f1_tempo, f2_custo]

# TODO 3: Configure o NSGA2 com pop_size=25 utilizando IntegerRandomSampling e RoundingRepair
# no crossover SBX e na mutacao PM (consulte o Exercicio 1 como referencia).
algorithm = NSGA2(
    pop_size=25,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True
)

# TODO 4: Execute a minimizacao por 35 geracoes (seed=10) e imprima as solucoes X e F.
res2 = minimize(KubernetesClusterProblem(), algorithm, termination=('n_gen', 35), seed=10)

ordem = np.argsort(res2.F[:, 0])
print(f"Soluções na fronteira: {len(res2.F)}")
print(" Réplicas | Nodes | Tempo (ms) | Custo (USD)")
for idx in ordem:
    sol_x, sol_f = res2.X[idx], res2.F[idx]
    print(f"   {sol_x[0]:2d}     |  {sol_x[1]:2d}   |   {sol_f[0]:6.2f}   |  US$ {sol_f[1]:7.2f}")

print("Amostra de 5 solucoes inteiras encontradas (Replicas, Nodes):")
for sol_x, sol_f in zip(res2.X[:5], res2.F[:5]):
    print(f"Replicas: {sol_x[0]:2d} | Nodes: {sol_x[1]:2d} => Tempo: {sol_f[0]:6.2f}ms | Custo: US$ {sol_f[1]:6.2f}")

plt.figure(figsize=(7, 4))
plt.scatter(res2.F[:, 0], res2.F[:, 1], color='purple', s=60, edgecolor='black')
plt.title("Exercicio 2 - Dimensionamento de Cluster Kubernetes")
plt.xlabel("Tempo de Resposta (ms) [Minimizar]")
plt.ylabel("Custo Mensal (US$) [Minimizar]")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()