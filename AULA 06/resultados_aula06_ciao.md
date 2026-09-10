# AULA 06

**Matriz inicial de feromônio:**

```python
[[1. 1. 1. 0. 0. 0.]
 [1. 1. 1. 1. 0. 0.]
 [1. 1. 1. 1. 1. 0.]
 [0. 1. 1. 1. 1. 1.]
 [0. 0. 1. 1. 1. 1.]
 [0. 0. 0. 1. 1. 1.]]
```

### **`Vizinhos do nó 0:** [1, 2]`

**`Vizinhos do nó 2:** [0, 1, 3, 4]`

**Rotas de teste (5 formigas antes do treino):**

```python
Formiga 1: [0, 1, 2, 3, 4, 5]
Formiga 2: [0, 1, 2, 3, 4, 5]
Formiga 3: [0, 1, 2, 4, 3, 5]
Formiga 4: [0, 1, 2, 4, 3, 5]
Formiga 5: [0, 1, 2, 3, 4, 5]
```

**Resultado final (50 iterações, 20 formigas):**

- Melhor rota encontrada: **[0, 1, 2, 3, 4, 5]**
- Melhor custo: **8.0** (2 + 1 + 2 + 1 + 2)
- Convergência: o melhor custo já apareceu na **1ª iteração** e se manteve estável até a 50ª — a rede é pequena o suficiente para que, mesmo com feromônio uniforme no início, uma das 20 formigas encontre a rota ótima de cara (BETA=2 já favorece fortemente arestas de baixo custo desde o começo).
- Matriz final de feromônio: ficou **totalmente concentrada** na rota ótima (feromônio = 500 em cada aresta do caminho 0→1→2→3→4→5, e 0 em todas as outras conexões) — a colônia "esqueceu" completamente as demais rotas.

### Perguntas — Lab01

**1. Por que o ACO utiliza várias formigas em vez de apenas uma? Qual a importância de explorar diferentes caminhos?**

Uma única formiga teria apenas a própria experiência como guia e, como as escolhas são probabilísticas, poderia repetir um caminho ruim por bastante tempo antes de encontrar um melhor. Sem outras formigas explorando alternativas em paralelo, a busca seria mais lenta e com maior risco de ficar presa em soluções ruins. Com várias formigas explorando a rede simultaneamente, o algoritmo cobre uma parte muito maior do espaço de possibilidades a cada iteração, aumentando a chance de que alguma encontre um caminho muito bom — e essa descoberta é rapidamente compartilhada com o restante da colônia por meio do feromônio.

**2. Por que uma rota de menor custo recebe mais feromônio? Como isso influencia as próximas formigas?**

O depósito é calculado como `Q / custo`; portanto, quanto menor o custo, maior o depósito. Essa é a forma de o algoritmo “premiar” boas soluções: rotas melhores se tornam mais atrativas para a próxima geração de formigas, que passam a escolhê-las com maior probabilidade. Forma-se, assim, um ciclo de retroalimentação positiva — bons caminhos atraem mais formigas, que reforçam ainda mais esses caminhos.

**3. O que aconteceria se não existisse evaporação do feromônio? Por que manter as primeiras informações para sempre poderia prejudicar a busca?**

Sem evaporação, o feromônio depositado nas primeiras iterações nunca diminuiria, só cresceria com o tempo. Assim, se as primeiras formigas encontrassem por acaso um caminho apenas razoável (não o melhor), esse caminho acumularia tanto feromônio que se tornaria quase impossível para as formigas seguintes escolherem outra opção, mesmo que existissem rotas melhores. A evaporação evita esse tipo de “viés histórico”, mantendo espaço para que novas descobertas concorram com o conhecimento acumulado.

---

## LABORATÓRIO 02 — Experimentando parâmetros

### Experimento 1 — ALPHA (influência da experiência acumulada)

| ALPHA | Melhor rota | Melhor custo | Comportamento do custo médio |
| --- | --- | --- | --- |
| 0.1 | [0,1,2,3,4,5] | 8.0 | **Nunca estabiliza** — oscila entre 8.5 e 10 até a iteração 50 |
| 1.0 | [0,1,2,3,4,5] | 8.0 | Converge suavemente por volta da iteração 15 |
| 5.0 | [0,1,2,3,4,5] | 8.0 | Converge quase imediatamente (iteração 2-3) |

**Pergunta:** Quando aumentamos o ALPHA, a influência da experiência acumulada aumenta ou diminui?

Aumenta bastante. Com ALPHA baixo (0.1), o feromônio quase não pesa na decisão: as formigas continuam escolhendo caminhos quase aleatoriamente mesmo após 50 iterações, ignorando o que a colônia já “aprendeu” (por isso o custo médio nunca estabiliza no gráfico). Já com ALPHA alto (5.0), pequenas diferenças de feromônio são fortemente amplificadas; assim, quando uma rota boa acumula um pouco mais de feromônio do que as demais, o enxame inteiro passa a segui-la quase exclusivamente. A convergência fica muito rápida, mas também aumenta a chance de o algoritmo “travar” cedo demais em uma solução que não seja a melhor possível (não é o caso aqui, pela simplicidade da rede, mas seria um risco em redes maiores).

### Experimento 2 — BETA (influência do custo)

| BETA | Melhor rota | Melhor custo | Comportamento do custo médio |
| --- | --- | --- | --- |
| 0.5 | [0,1,2,4,5] | 8.0 | Converge por volta da iteração 15 |
| 2.0 | [0,1,2,3,4,5] | 8.0 | Converge por volta da iteração 10 |
| 5.0 | [0,1,2,3,4,5] | 8.0 | Converge quase imediatamente |

Confirma exatamente o que o roteiro antecipa: BETA baixo faz o custo pesar menos na decisão (mais exploração, convergência mais lenta), enquanto BETA alto faz caminhos de menor custo dominarem a escolha quase imediatamente.

### Experimento 3 — Taxa de evaporação

| TAXA_EVAPORACAO | Melhor custo | Comportamento do custo médio |
| --- | --- | --- |
| 0.1 | 8.0 | Converge por volta da iteração 10, mas com pequenas oscilações residuais depois disso |
| 0.5 | 8.0 | Converge de forma limpa por volta da iteração 8 |
| 0.9 | 8.0 | Converge de forma mais limpa e ligeiramente mais rápida |

**Pergunta:** O que acontece quando o algoritmo esquece rapidamente as experiências anteriores (evaporação alta)?

Com evaporação alta (0.9), o feromônio antigo é quase todo removido a cada iteração; assim, o reforço mais recente passa a ser o que realmente importa. Isso faz o enxame reagir rapidamente a qualquer caminho bom recém-descoberto, mas também exige que a mesma rota seja “reconquistada” continuamente para se manter relevante. Já com evaporação baixa (0.1), o feromônio se acumula e persiste por mais tempo, mantendo escolhas antigas influentes por mais iterações, mesmo sem reforço recente. Na prática, observam-se pequenas oscilações residuais nesse cenário, sinal de que o “esquecimento” mais lento permite que rotas ligeiramente piores continuem competindo por mais tempo.

### Experimento 4 — Número de formigas

| NUM_FORMIGAS | Melhor custo | Comportamento do custo médio |
| --- | --- | --- |
| 5 | 8.0 | Converge por volta da iteração 6, com mais ruído (poucas amostras por iteração) |
| 20 | 8.0 | Converge por volta da iteração 6-7, de forma mais estável |
| 50 | 8.0 | Converge ainda mais rápido e com curva mais suave |

---

## LABORATÓRIO 03 — Completando o ACO

- Atratividade 0→1 (custo 2): **0.25**
- Atratividade 0→2 (custo 4): **0.0625**

**Resultado da execução completa (50 iterações, 20 formigas):**

- Melhor rota: **[0, 1, 2, 3, 4, 5]**
- Melhor custo: **8.0**

O resultado bate exatamente com o Lab01, como esperado, as funções implementadas (`calcular_atratividade`, `evaporar_feromonio`, `depositar_feromonio`, `construir_rota`) reproduzem a mesma lógica, apenas organizadas em funções separadas.

**1. Por que a fórmula da atratividade utiliza 1/custo em vez do custo diretamente?**

Porque queremos que **caminhos mais baratos sejam mais atrativos**. Se usássemos o custo diretamente, um custo alto geraria uma atratividade alta, favorecendo justamente os piores caminhos — o oposto do que queremos. Ao inverter (1/custo), um custo baixo produz um valor grande, e um custo alto produz um valor pequeno, alinhando a fórmula ao objetivo de minimizar o custo total da rota.

**2. O que acontece com a atratividade quando uma rota recebe mais feromônio?**

Como a atratividade é `feromônio^ALPHA × (1/custo)^BETA`, um aumento no feromônio eleva diretamente o valor da atratividade dessa aresta (assumindo ALPHA > 0). Isso aumenta a probabilidade de a aresta ser escolhida nas próximas construções de rota, mesmo que seu custo isolado não seja o menor — é assim que o "aprendizado coletivo" da colônia, ao longo do tempo, consegue superar a informação de custo pura.

**3. Por que `construir_rota()` precisa impedir revisitar um nó já presente na rota?**

Sem essa restrição, a formiga poderia entrar em um laço infinito, ficando presa alternando entre os mesmos nós para sempre (por exemplo, indo e voltando entre dois nós vizinhos), sem nunca progredir em direção ao destino. Além disso, permitir revisitas geraria rotas com custo artificialmente inflado (percorrendo o mesmo trecho várias vezes) ou logicamente sem sentido para o problema de encontrar o **caminho** mais barato entre origem e destino.

---

## LABORATÓRIO 04

Implementação própria, organizada como uma classe `ColoniaACO`, atendendo aos 12 requisitos do sistema listados no roteiro (matriz de custos, matriz de feromônio, criação de formigas, construção de rota sem revisitas, cálculo de custo, reforço das melhores rotas, evaporação, repetição por iterações, e relatório de melhor rota/custo/gráfico de convergência).

**Resultado principal (parâmetros mínimos do roteiro):**

- Melhor rota encontrada: **[0, 1, 2, 3, 4, 5]**
- Melhor custo: **8.0**

**Variação de parâmetros testada:**

| Configuração | Parâmetros | Melhor rota | Melhor custo |
| --- | --- | --- | --- |
| Base | formigas=20, iter=50, α=1.0, β=2.0, evap=0.5 | [0,1,2,3,4,5] | 8.0 |
| Mais formigas, menos iterações | formigas=50, iter=20, α=1.0, β=2.0, evap=0.5 | [0,1,2,3,4,5] | 8.0 |
| Alpha baixo (mais exploração) | formigas=20, iter=50, α=0.2, β=2.0, evap=0.5 | [0,1,2,3,4,5] | 8.0 |
| Beta alto (guloso) | formigas=20, iter=50, α=1.0, β=6.0, evap=0.5 | [0,1,2,3,4,5] | 8.0 |
| Evaporação alta | formigas=20, iter=50, α=1.0, β=2.0, evap=0.9 | [0,1,2,4,5] | 8.0 |

### Perguntas

**1. Explique como o feromônio ajuda o ACO a aprender quais caminhos são melhores.**

O feromônio funciona como uma memória coletiva e indireta: cada formiga que percorre uma rota deixa um rastro proporcional à qualidade dessa rota (quanto menor o custo, maior o rastro). As formigas seguintes não precisam saber *por que* um caminho é bom, elas simplesmente são atraídas por onde há mais feromônio. Com o tempo, esse mecanismo de retroalimentação faz os caminhos bons acumularem cada vez mais feromônio (mais formigas os escolhem → mais reforço → ainda mais formigas os escolhem), enquanto caminhos ruins, por receberem pouco reforço e ainda sofrerem evaporação, gradualmente perdem relevância. Trata-se de um aprendizado emergente e descentralizado: nenhuma formiga individual “sabe” qual é o melhor caminho, mas o comportamento coletivo converge para ele.

**2. Qual a diferença entre explorar novos caminhos e aproveitar caminhos que já demonstraram ser bons?**

**Explorar** (exploration) significa testar rotas diferentes das já conhecidas, mesmo sem garantia de que sejam boas, é o que permite ao algoritmo descobrir soluções melhores que ainda não foram tentadas. **Aproveitar** (exploitation/explotação) significa reforçar e seguir os caminhos que já se mostraram bons, refinando o que já se sabe. O ACO equilibra as duas estratégias por meio dos parâmetros: BETA e o feromônio acumulado favorecem a explotação (seguir o que já parece bom), enquanto a escolha probabilística (em vez de sempre escolher o melhor caminho com certeza) e a evaporação preservam uma margem de exploração. Um bom algoritmo de otimização precisa desse equilíbrio, só explorar não refina a solução; só aproveitar aumenta o risco de ficar preso em um ótimo local, sem descobrir algo melhor.

**3. Para melhorar o desempenho desse ACO numa rede muito maior, qual parâmetro ou parte do algoritmo você investigaria primeiro? Justifique.**

Investigaria primeiro o **equilíbrio entre ALPHA, BETA e a taxa de evaporação** em conjunto, e não um parâmetro isolado, nos experimentos do Lab02 ficou claro que esses fatores interagem: ALPHA ou evaporação muito baixos fazem o algoritmo “andar em círculos” sem convergir (o custo médio não estabiliza), enquanto valores muito altos levam o enxame a convergir rápido demais, o que, em uma rede grande e complexa (com muitos ótimos locais), é arriscado o algoritmo pode travar cedo em uma rota medíocre, antes de explorar o suficiente.

Em segundo lugar, investigaria o **número de formigas e de iterações**: em uma rede maior, o espaço de busca cresce muito, e o Experimento 4 do Lab02 já mostrou que mais formigas reduzem a variância e aceleram a convergência, porém com custo computacional, que precisa ser balanceado (mais formigas ou mais iterações significam mais tempo de execução).

Por fim, também valeria investigar otimizações estruturais, como limitar a atratividade a um subconjunto dos vizinhos mais promissores em vez de avaliar todos (técnica comum em implementações de ACO para grafos grandes), para reduzir o custo computacional por iteração.
