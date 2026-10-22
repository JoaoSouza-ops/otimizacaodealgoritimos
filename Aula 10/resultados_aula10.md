##Resultados da Aula 10

## a) Desafio dos Extremos

### Resultados medidos

| Configuração | (0, 0) | (100, 10) | (50, 5) | Maior salto na malha 41×41 |
|---|---|---|---|---|
| Centroide + `trimf` (base) | 10,00 | 90,00 | 70,00 | 17,95 |
| **A:** Centroide + `trapmf` na Crítica | 10,00 | 90,71 | 70,00 | 17,95 |
| **B:** MOM + `trimf` | **0,00** | **100,00** | 70,00 | **59,76** |
| C: Centroide + `trapmf` estreito nas duas pontas | 10,04 | 89,96 | 70,00 | 17,77 |
| A + calibração linear da saída | **0,00** | **100,00** | 74,34 | 22,24 |

### 1. Por que o Centroide com triângulos não atinge 0% nem 100%?

Em (0, 0) só a regra *Impacto Baixo ∧ Explorabilidade Baixa → Urgência Baixa* dispara, com grau 1. O resultado da agregação é o triângulo inteiro de "Baixa". O centroide é o **centro de massa de toda a área**, não o ponto de maior pertinência. Como o triângulo `[0,0,30]` se estende até 30, seu centro de massa fica em 30/3 = 10. O mesmo ocorre no topo: o triângulo `[70,100,100]` tem centroide (70+100+100)/3 = 90. A área sempre tem largura positiva, então o centroide fica estritamente no interior do universo e **nunca** coincide com 0 ou 100. Isso é uma propriedade matemática do método, não um erro de código.

### 2. O que muda com `trapmf` na Urgência Crítica?

O trapézio `[75,90,100,100]` cria um platô de pertinência 1 entre 90 e 100, e a massa se desloca para a borda. O centroide sobe de 90,00 para **90,71**, um ganho pequeno. Em (0, 0) nada muda (10,00), pois a Baixa continua com a mesma largura. A superfície continua suave (maior salto idêntico ao da base, 17,95). Estreitar o trapézio nas duas pontas (abordagem C) não resolve: o centroide é calculado sobre o conjunto inteiro, e a base larga continua dominando (10,04 e 89,96). Somente o formato do trapézio não basta para chegar aos extremos.

### 3. O que muda com MOM (Mean of Maximum)?

O MOM usa só a média dos pontos onde a pertinência agregada é máxima, ignorando o resto da área. Em (0, 0) o platô de máximo começa em 0, e o resultado é **0,00%**. Em (100, 10) o máximo está em 100, e o resultado é **100,00%**, cravando os extremos. O custo é a suavidade: o MOM só enxerga o conjunto dominante, e quando a regra dominante muda a saída salta de um conjunto para outro. O maior salto entre pontos vizinhos da malha é **59,76**, contra ~18 do centroide, e a superfície fica em degraus (ver `comparacao_superficies.png`).

### Qual abordagem é mais recomendável?

- **MOM (B):** crava 0% e 100%, mas **não preserva a suavidade**. Pequenas variações de Impacto ou Explorabilidade podem causar saltos grandes de urgência, o que é ruim para um sistema de priorização de incidentes.
- **Trapézio (A):** **preserva a suavidade**, mas **não crava** os extremos (90,71%).
- **Recomendação:** manter o **Centroide** (superfície contínua) e, se o requisito for ter 0% e 100% exatos, usar `trapmf` mais uma **calibração linear** da saída. A calibração mapeia a saída de (0, 0) para 0 e a de (100, 10) para 100. É monotônica, e a medição confirmou 0,00 e 100,00 nos extremos com maior salto de 22,24 (contra 59,76 do MOM). A calibração é uma pós-correção externa ao motor Mamdani, e o grau de severidade intermediário muda um pouco (50, 5 → 74,34). Se o requisito for apenas uma ordenação coerente de prioridades, o centroide puro já atende. O ponto central do desafio é que a preservação da suavidade e o travamento exato nos extremos são objetivos em tensão no defuzzificador.

## b) Matriz de Regras 3×3 (9 regras, sem lacunas de cobertura)

| Impacto \ Explorabilidade | Baixa (0–4) | Moderada (2–8) | Alta (6–10) |
|---|---|---|---|
| **Baixo (0–40)** | Urgência Baixa | Urgência Baixa | Urgência Média |
| **Médio (20–80)** | Urgência Média | Urgência Alta | Urgência Alta |
| **Alto (60–100)** | Urgência Crítica | Urgência Crítica | Urgência Crítica |

As sobreposições das funções de entrada (20–40, 60–80 em Impacto; 2–4, 6–8 em Explorabilidade) garantem que, em qualquer ponto do universo, ao menos uma regra dispare (`assert len(regras) == 9` no código).

## c) Análise da Superfície de Decisão 3D (`superficie_decisao.png`)

Configuração: Centroide + `trapmf` na Urgência Crítica, malha 51×51.

- **Continuidade:** não há buracos nem degraus abruptos. A transição entre conjuntos de saída é gradual, graças às sobreposições das entradas e à agregação Mamdani.
- **Monotonicidade:** a urgência cresce com o Impacto e com a Explorabilidade, como esperado pela matriz de regras.
- **Dominância do Impacto:** para Impacto alto (≥ 80) a urgência fica em um platô próximo de 90%, independentemente da Explorabilidade, pois as 3 regras da linha "Alto" produzem Crítica.
- **Região baixa:** com Impacto baixo e Explorabilidade baixa, a urgência fica perto de 10% (mínimo da superfície).
- **Inclinação máxima:** ocorre na faixa de Impacto entre 40 e 60 combinada com Explorabilidade moderada a alta, onde as regras Média, Alta e Crítica competem.
- **Limites:** a superfície vai de ~10% a ~90,7%, nunca 0% ou 100%, o efeito do centroide discutido acima.
