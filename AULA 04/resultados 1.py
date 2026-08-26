import numpy as np

def calcular_custo(rota, matriz): 
    dist = 0 
    for i in range(len(rota)-1): dist += matriz[rota[i], rota[i+1]] 

    return dist + matriz[rota[-1], rota[0]]

#Modifique para False para testar a execução sem elitismo

USAR_ELITISMO = True

NUM_NOS = 8 
matriz_teste = np.random.uniform(10, 100, (NUM_NOS, NUM_NOS)) 
TAM_POP = 40 
GERACOES = 80

populacao = [np.random.permutation(NUM_NOS) for _ in range(TAM_POP)]

for g in range(GERACOES): 
    custos = [calcular_custo(ind, matriz_teste) 
        for ind in populacao] 
    melhor_idx = np.argmin(custos)

novos = []
if USAR_ELITISMO:
    novos.append(populacao[melhor_idx].copy())
    
while len(novos) < TAM_POP:
    i1, i2 = np.random.choice(TAM_POP, 2, replace=False)
    pai = populacao[i1] if custos[i1] < custos[i2] else populacao[i2]
    
    filho = pai.copy()
    if np.random.rand() < 0.3:
        idx1, idx2 = np.random.choice(NUM_NOS, 2, replace=False)
        filho[idx1], filho[idx2] = filho[idx2], filho[idx1]
    novos.append(filho)
    
populacao = novos

custos_finais = [calcular_custo(ind, matriz_teste) 
for ind in populacao]
print(f"[Exercício 1] Menor Custo Obtido (Elitismo={USAR_ELITISMO}) {min(custos_finais):.2f}")