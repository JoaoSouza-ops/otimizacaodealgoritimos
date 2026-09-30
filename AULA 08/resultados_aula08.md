Resultados da Aula 08

LAB 1:
Referencia (otimo analitico LP): W = [0.2183 0.2619 0.031  0.3056 0.1833 0.    ]  obj = 38.4619

C = [42. 35. 58. 30. 50. 65.]

Pop   | Melhor W                                       | Obj (C)   | Fitness   | T_max(C)  | sum(w)   | Valido
10    | [0.2183 0.2619 0.0329 0.3056 0.1814 0.    ]    | 38.4776   | 38.4777   | 75.000    | 1.000000 | OK
30    | [0.2182 0.2619 0.031  0.3056 0.1833 0.    ]    | 38.4621   | 38.4621   | 75.000    | 1.000000 | OK
50    | [0.2183 0.2619 0.031  0.3056 0.1833 0.    ]    | 38.4619   | 38.4619   | 75.000    | 1.000000 | OK

Fitness final (30 execucoes): media +- desvio
  10 particulas: 38.6879 +- 0.2039 (melhor 38.4777)
  30 particulas: 38.5140 +- 0.0917 (melhor 38.4621)
  50 particulas: 38.4887 +- 0.0647 (melhor 38.4619)

Fitness medio (30 execucoes) em iteracoes selecionadas:
  10 part: {1: 19245.4, 5: 241.44, 10: 40.696, 25: 39.55, 50: 39.043, 100: 38.82, 200: 38.688}
  30 part: {1: 2312.034, 5: 40.568, 10: 39.585, 25: 38.945, 50: 38.707, 100: 38.568, 200: 38.514}
  50 part: {1: 560.725, 5: 40.132, 10: 39.387, 25: 38.833, 50: 38.606, 100: 38.511, 200: 38.489}




  LAB 2 :
  Otimo global (forca bruta 2^15): valor=315  servicos=['S2', 'S4', 'S5', 'S7', 'S10', 'S13', 'S14']  RAM=16.0 CPU=7.5

Estrategia             | Melhor valor | Media+-dp    | Acertos    | Div. final | Div. media  
A (rigida)             | 315          | 314.2+-1.9   | 25/30      | 0.248      | 0.293       
B (proporcional)       | 315          | 314.8+-0.9   | 29/30      | 0.264      | 0.298       

Estrategia A: melhor combinacao = ['S2', 'S4', 'S5', 'S7', 'S10', 'S13', 'S14'], valor=315, RAM=16.0GB, CPU=7.5; runs cujo melhor individuo final e viavel: 100%

Estrategia B: melhor combinacao = ['S2', 'S4', 'S5', 'S7', 'S10', 'S13', 'S14'], valor=315, RAM=16.0GB, CPU=7.5; runs cujo melhor individuo final e viavel: 100%

Fracao media de individuos viaveis na populacao (gen 0 / 10 / 40 / 79):
  A: [0.14, 0.619, 0.611, 0.624]
  B: [0.14, 0.53, 0.571, 0.577]

Media/dp do fitness (media de 30 runs) gen 0 / 10 / 40 / 79:
  A: [(33.3, 83.6), (152.3, 124.8), (160.8, 131.9), (165.5, 132.4)]
  B: [(72.6, 104.2), (199.8, 101.4), (208.0, 105.4), (212.7, 104.5)]




  Pares criticos (i, j, peso): [(2, 3, 5), (3, 8, 3), (3, 5, 2), (7, 9, 5), (1, 6, 2), (5, 7, 1), (3, 6, 3), (4, 8, 4), (0, 6, 1), (0, 9, 3), (5, 8, 1), (0, 3, 4)]

Matriz de latencias D (us):
[[  0.   29.2  88.6  36.7  66.6  65.3  42.5  41.2  45.5  22. ]
 [ 29.2   0.   83.3  15.2  79.1  55.9  26.9  64.7  72.3   9.3]
 [ 88.6  83.3   0.   71.3  54.6  30.1  59.1  84.6 104.1  83. ]
 [ 36.7  15.2  71.3   0.   73.7  43.5  14.3  66.3  77.1  18.8]
 [ 66.6  79.1  54.6  73.7   0.   55.5  65.6  40.6  59.6  74.3]
 [ 65.3  55.9  30.1  43.5  55.5   0.   31.2  72.3  90.2  56.4]
 [ 42.5  26.9  59.1  14.3  65.6  31.2   0.   64.8  78.4  28.5]
 [ 41.2  64.7  84.6  66.3  40.6  72.3  64.8   0.   21.8  57.8]
 [ 45.5  72.3 104.1  77.1  59.6  90.2  78.4  21.8   0.   65. ]
 [ 22.    9.3  83.   18.8  74.3  56.4  28.5  57.8  65.    0. ]]

Matriz de ADJACENCIA final (melhor run do ACO):
[[0 0 0 0 0 0 0 0 0 1]
 [0 0 0 1 0 0 0 0 0 1]
 [0 0 0 1 0 0 0 0 0 0]
 [0 1 1 0 0 1 1 0 1 0]
 [0 0 0 0 0 0 0 0 1 0]
 [0 0 0 1 0 0 0 0 0 0]
 [0 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 1]
 [0 0 0 1 1 0 0 0 0 0]
 [1 1 0 0 0 0 0 1 0 0]]

Arestas: [(0, 9), (1, 3), (1, 9), (2, 3), (3, 5), (3, 6), (3, 8), (4, 8), (7, 9)]
Arvore valida (N-1 arestas, conexa, sem ciclos): True

Custo (latencia ponderada entre pares criticos):
  Topologia aleatoria - media de 2000 arvores : 5345.6 (dp 1293.8, melhor 2336.1)
  MST (Kruskal, so cabeamento)                : 2066.0
  ACO - melhor run                            : 1863.3
  ACO - 20 runs                               : 1914.8 +- 23.2

Ganho de reducao de latencia do ACO vs aleatoria:
  melhor run : 65.14%
  media runs : 64.18%
  vs MST     : 9.81%
Cabeamento total: ACO=370.1 us, MST=225.7 us
