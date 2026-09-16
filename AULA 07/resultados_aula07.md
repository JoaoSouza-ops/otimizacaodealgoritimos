
---

## LAB 01 — ACO com Busca Local (Exploration vs. Exploitation)

**Output da execução:**

```
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70
```

<img width="563" height="455" alt="image" src="https://github.com/user-attachments/assets/631c9bee-e031-4496-9df2-9cd497bbb8d5" />

### Perguntas — Lab 01

**1. Como o uso da busca local 2-opt afeta o equilíbrio entre Exploration e Exploitation na busca de caminhos?**

O 2-opt desloca fortemente o equilíbrio para a **Exploitation (explotação),** em vez de manter a rota bruta construída pela formiga que pode conter cruzamentos ou trechos ineficientes devido às escolhas probabilísticas, o 2-opt a refina localmente até não haver mais melhorias possíveis com trocas simples de segmentos. Assim, cada solução que atualiza o feromônio já é a “melhor versão possível” daquela rota específica, fazendo com que o feromônio represente caminhos de qualidade muito mais alta do que representaria em um ACO puro.

A Exploration ainda existe, mas o 2-opt reduz o impacto de rotas ruins antes que elas influenciem o aprendizado coletivo e por isso, nesta rede pequena, o algoritmo encontrou o ótimo já na primeira iteração.

**2. O que aconteceria com a convergência do algoritmo se a taxa de evaporação (rho) fosse definida em 0.0 (sem evaporação)?**

Sem evaporação, todo feromônio depositado seria permanente e apenas cumulativo.

Isso aceleraria bastante a convergência inicial (o primeiro caminho bom encontrado ganha vantagem e nunca perde força), mas tornaria o algoritmo extremamente vulnerável a ficar preso em ótimos locais. Se as primeiras formigas encontrassem por acaso uma rota apenas razoável, o feromônio ali acumulado (sempre crescente, nunca decrescente) dominaria rapidamente as escolhas futuras, praticamente eliminando a chance de outras rotas, mesmo melhores, serem descobertas depois.

---

## LAB 02 — Algoritmo Genético: Seleção, Crossover e Mutação

**Output da execução (seed=42):**

```
[LAB 02] Execução completa
Melhor fitness por geração: [13, 14, 15, 15, 15, 15, 15, 14, 13, 15]
Melhor indivíduo encontrado: [0 1 1 1 1]
Peso total: 8
Valor total (fitness): 15
```

### Perguntas — Lab 02

**1. Explique qual é o papel do operador de Mutação em um Algoritmo Genético e o que ocorre se a taxa de mutação for configurada em 100%.**

A mutação introduz variação aleatória nos genes dos indivíduos, permitindo que o algoritmo explore regiões do espaço de busca que a seleção e o crossover sozinhos não alcançariam (que só recombinam material genético já existente na população). Ela é o principal mecanismo de diversidade genética e evita que a população convirja cedo demais para soluções sub-ótimas por falta de "material novo". Se a taxa de mutação fosse 100%, porém, todo gene de todo indivíduo seria invertido em toda geração**,** isso destruiria completamente qualquer estrutura útil herdada dos pais, tornando cada nova geração essencialmente aleatória e eliminando qualquer benefício da seleção e do crossover. Na prática, o algoritmo deixaria de ser genético e se tornaria uma busca aleatória pura, sem aprendizado ao longo das gerações.

**2. Por que a penalização do fitness (atribuir 0 para indivíduos que estouram a capacidade) é fundamental para a convergência das restrições?**

Sem essa penalização, indivíduos inválidos (que estouram o peso máximo) poderiam ter fitness alto simplesmente por incluir muitos itens de valor, mesmo sendo soluções inviáveis para o problema real. Isso faria a seleção por torneio favorecer esses indivíduos "trapaceiros", direcionando toda a população para soluções que violam a restrição de peso. Ao zerar o fitness de qualquer indivíduo inválido, o algoritmo é forçado a competir apenas dentro do espaço de soluções viáveis. 

---

## LAB 03 — PSO: Inércia, Componente Cognitiva e Social

```
[LAB 03] Melhor posição encontrada pelo Enxame (gbest): [ 0.00742668 -0.0130891 ]
[LAB 03] Fitness do gbest: 0.000226
```

### Perguntas — Lab 03

**1. O que acontece com o comportamento das partículas se zerarmos a componente cognitiva (c₁ = 0)?**

Com c₁=0, cada partícula deixa de "confiar" na própria melhor experiência (pbest) e passa a se mover apenas em função da inércia e da atração pelo gbest (melhor posição do enxame inteiro). Isso faz todas as partículas convergirem rapidamente para a vizinhança do gbest, reduzindo bastante a diversidade de busca. O enxame passa a se comportar quase como um único "bando" seguindo um líder, em vez de vários exploradores independentes. O risco é convergência prematura: se o gbest estiver preso em um mínimo local, não há mais nenhuma força individual puxando as partículas para longe dele.

**2. Qual a função do parâmetro de Inércia (w) na busca por mínimos globais?**

A inércia controla o quanto a partícula mantém sua direção de movimento anterior. Valores altos de w favorecem a exploração (a partícula continua se deslocando amplamente pelo espaço de busca, "resistindo" a mudanças bruscas de direção), enquanto valores baixos favorecem a explotação/refinamento (a partícula freia mais rápido perto de uma boa posição, permitindo ajuste fino). O valor de w=0.5 usado aqui é intermediário, o que explica a convergência suave e relativamente rápida observada no experimento, nem exploração excessiva, nem parada prematura.

---

## LAB 04 — ACO: Feromônio, Evaporação e Atratividade

**Output da execução:**

```
[LAB 04] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]
```

**Atratividade inicial (η = 1/latência) por enlace:**

```
[[0.     0.2    0.5    0.1111]
 [0.2    0.     0.3333 1.    ]
 [0.5    0.3333 0.     0.1429]
 [0.1111 1.     0.1429 0.    ]]
```

### Perguntas — Lab 04

**1. Por que a evaporação do feromônio é necessária no algoritmo ACO?**

A evaporação impede que decisões antigas dominem para sempre a busca. Sem ela, o feromônio depositado nas primeiras iterações só cresceria, tornando cada vez mais improvável que a colônia explore alternativas, mesmo que existam caminhos melhores ainda não descobertos. A evaporação atua como um "esquecimento gradual", equilibrando o conhecimento acumulado (exploitation) com a necessidade de continuar testando novas possibilidades (exploration).

**2. O que ocorreria em grafos complexos sem ela? Qual a relação matemática entre a latência de um enlace e sua atratividade inicial (eta) para as formigas?**

Em grafos complexos (muitos nós e múltiplos ótimos locais), a ausência de evaporação tornaria o algoritmo extremamente suscetível à convergência prematura: os primeiros caminhos razoáveis encontrados acumulariam feromônio de forma irreversível, e a colônia inteira convergiria para eles antes de explorar o espaço de busca de forma significativa, resultando tipicamente em soluções bem piores que o ótimo real, especialmente em redes grandes onde a chance de as primeiras formigas acharem por acaso a melhor rota é baixa.

A relação matemática entre latência e atratividade inicial é de **proporcionalidade inversa**: η = 1/latência. Quanto menor a latência de um enlace, maior sua atratividade. Um enlace de latência 1 tem atratividade η=1.0 (a maior da matriz), enquanto um de latência 9 tem atratividade η≈0.111 (a menor). Essa é a heurística "gulosa" do ACO: na ausência de qualquer feromônio acumulado, as formigas já tendem a preferir os enlaces de menor custo/latência.

---

## LAB 05 — Memético: Meta-heurística + Busca Local

**Output da execução (seed=42):**

```
[LAB 05] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
[LAB 05] Solução Refinada: [ 2.47553974 -3.04650038] | Fitness: 35.7154
```

**Variabilidade em 5 execuções independentes** (mesmo ponto inicial, hill climbing é estocástico):

```
Execução 1: fitness final = 35.4364
Execução 2: fitness final = 36.5582
Execução 3: fitness final = 36.3045
Execução 4: fitness final = 36.1327
Execução 5: fitness final = 36.3893
```

### Perguntas — Lab 05

**1. Qual a diferença fundamental de conceito entre um Algoritmo Genético Puro e um Algoritmo Memético?**

Um Algoritmo Genético puro depende inteiramente dos operadores populacionais (seleção, crossover, mutação) para refinar soluções ao longo das gerações,  a melhoria acontece de forma "coletiva e lenta", através de recombinação e variação aleatória. Um Algoritmo Memético combina essa busca populacional (exploração global) com uma etapa adicional de busca local determinística ou estocástica aplicada a cada indivíduo (como o hill climbing implementado neste laboratório) uma forma de "aprendizado individual" que refina cada solução antes ou depois dos operadores genéticos atuarem. Isso combina exploração global (do GA) com explotação local intensiva (da busca local), geralmente acelerando bastante a convergência para soluções de alta qualidade.

**2. Em termos de custo computacional, qual o impacto de executar a busca local sobre todos os indivíduos de uma população a cada geração?**

O custo computacional cresce multiplicativamente: se a busca local tem custo O(k) por indivíduo, aplicá-la a toda uma população de tamanho N a cada uma das G gerações custa O(N × G × k) avaliações de fitness adicionais, além do custo já existente do GA. Em problemas com função de fitness cara de avaliar (como simulações complexas), isso pode tornar o algoritmo memético proibitivamente lento. Por isso, na prática, é comum aplicar a busca local apenas a uma fração da população (ex: só aos melhores indivíduos de cada geração) ou usar critérios de parada mais agressivos na busca local, para equilibrar qualidade de solução com tempo de execução.
