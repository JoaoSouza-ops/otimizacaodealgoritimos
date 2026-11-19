# Resultados da Aula 13 
## Respostas de Auditoria (AC-4 Parte Final)

### a) Diferença prática observada entre variáveis contínuas e inteiras (`IntegerRandomSampling` e `RoundingRepair`)


- Para variáveis continuas o NSGA-II opera gerando soluções com casas decimais e emboram formem uma Fronteira de Parero continua e suave, essas soluções exigem arredondamento manual posterior o que pode violar restrições pu tirá-las da fronteira ótima. 
- Para variaveis inteiras, o população já nasce apenas com valores inteiro e a cada geração, os filhos gerados pelos operadoores e mutação passam pelo arredondamento antes da avaliação. Na prática, isso produz uma fronteira de pareto onde todas as soluções são diretamente aplicáveis no mundo real. 


### b) Valores numéricos de Hipervolume obtidos no Exercício 4 (10 gerações vs. 80 gerações)
- **Ponto de referência (`ref_point`):** `[400.0, 600.0]`
- **Hipervolume com 10 gerações (`hv_10_gen`):** `226626.7047731528`
- **Hipervolume com 80 gerações (`hv_80_gen`):** `226715.93778257925`
- **Análise:** O Hipervolume maior em 80 gerações comprova quantitativamente que a evolução por mais gerações aproximou a Fronteira de Pareto dos valores mínimos ideais e aumentou a área dominada pelas soluções encontradas.


### c) Escala hospitalar recomendada pelo MCDM no Exercício 6 (Pesos: 40% Custo / 60% Tempo de Espera)
- **Médicos Plantonistas (`x1`):** `17` médicos
- **Enfermeiros (`x2`):** `32` enfermeiros
- **Custo do Plantão (`f1_custo`):** `R$ 34800.00`
- **Tempo Médio de Espera (`f2_espera`):** `18.09 minutos` *(Respeitando a restrição de SLA `f2_espera <= 25.0` min, ou seja, `G <= 0`)*.


---

## Execução dos Exercícios Práticos

# === EXERCÍCIO 1: Variáveis Inteiras na Prática (SOC Autônomo) ===

 Amostra de 5 solucoes inteiras encontradas (Pods, Analistas):
Pods: 30 | Analistas: 15 => Latencia:  23.33ms | Custo: R$ 1215.00
Pods:  1 | Analistas:  1 => Latencia: 550.00ms | Custo: R$  63.00
Pods:  2 | Analistas:  1 => Latencia: 350.00ms | Custo: R$  81.00
Pods:  3 | Analistas:  1 => Latencia: 283.33ms | Custo: R$  99.00
Pods:  4 | Analistas:  1 => Latencia: 250.00ms | Custo: R$ 117.00

<img width="626" height="393" alt="image" src="https://github.com/user-attachments/assets/0b21f101-9699-4200-9043-21fd681ed3fd" />


# === EXERCÍCIO 2: Dimensionamento Inteiro de Cluster Kubernetes ===
 Soluções na fronteira: 25
 Réplicas | Nodes | Tempo (ms) | Custo (USD)
   40     |  12   |    31.67   |  US$ 1500.00
   40     |  11   |    33.18   |  US$ 1415.00
   39     |   9   |    37.61   |  US$ 1233.00
   33     |   8   |    43.18   |  US$ 1076.00
   39     |   5   |    55.38   |  US$  893.00
   32     |   5   |    58.75   |  US$  809.00
   20     |   6   |    63.33   |  US$  750.00
   20     |   5   |    70.00   |  US$  665.00
   16     |   5   |    77.50   |  US$  617.00
   13     |   5   |    86.15   |  US$  581.00
   11     |   5   |    94.55   |  US$  557.00
   16     |   3   |   104.17   |  US$  447.00
   13     |   3   |   112.82   |  US$  411.00
   18     |   2   |   133.33   |  US$  386.00
   13     |   2   |   146.15   |  US$  326.00
   10     |   2   |   160.00   |  US$  290.00
    7     |   2   |   185.71   |  US$  254.00
    5     |   2   |   220.00   |  US$  230.00
    4     |   2   |   250.00   |  US$  218.00
    8     |   1   |   275.00   |  US$  181.00
    6     |   1   |   300.00   |  US$  157.00
    5     |   1   |   320.00   |  US$  145.00
    4     |   1   |   350.00   |  US$  133.00
    3     |   1   |   400.00   |  US$  121.00
    2     |   1   |   500.00   |  US$  109.00
Amostra de 5 solucoes inteiras encontradas (Replicas, Nodes):
Replicas:  2 | Nodes:  1 => Tempo: 500.00ms | Custo: US$ 109.00
Replicas: 40 | Nodes: 12 => Tempo:  31.67ms | Custo: US$ 1500.00
Replicas:  3 | Nodes:  1 => Tempo: 400.00ms | Custo: US$ 121.00
Replicas:  4 | Nodes:  1 => Tempo: 350.00ms | Custo: US$ 133.00
Replicas: 33 | Nodes:  8 => Tempo:  43.18ms | Custo: US$ 1076.00

<img width="626" height="393" alt="image" src="https://github.com/user-attachments/assets/d3864779-56d9-4939-a0c6-25dae744370f" />

# === EXERCÍCIO 3: Operadores Genéticos (Exploração vs. Explotação) ===

<img width="695" height="470" alt="image" src="https://github.com/user-attachments/assets/f103a9bd-297a-4537-a665-3930cef17adc" />

# === EXERCÍCIO 4: Avaliando Qualidade com Hipervolume (HV) ===

Hipervolume (10 geracoes): 226626.7047731528
Hipervolume (80 geracoes): 226715.93778257925

# === EXERCÍCIO 5: Tomada de Decisão Automática (MCDM - PseudoWeights) ===

 Decisao Recomendada (Pesos 30% Custo / 70% Performance):
-> Configuracao: 76.6 GB RAM | 2755 IOPS
-> Resultado:    US$ 56.52/h | Tempo de Query: 8.06 ms

<img width="695" height="470" alt="image" src="https://github.com/user-attachments/assets/e173a8d5-694b-4ad5-a722-53de86510e5c" />

# === EXERCÍCIO 6: Pipeline Completo - Otimização + Restrição + MCDM ===

Escala Hospitalar Recomendada (MCDM - 40% Custo / 60% Tempo de Espera):
-> Médicos Plantonistas: 17
-> Enfermeiros:          32
-> Custo do Plantão:     R$ 34800.00
-> Tempo de Espera:      18.09 min (Restrição SLA <= 25.0 min)
