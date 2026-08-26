## LAB 04

RESULTADOS — MOTOR DE DECISIONING SD-WAN ZERO-TRUST
======================================================================
Rota selecionada: [ 0 10  2  3  6  4  1  9  7  5  8 11]
Latência total: 150.42 ms
Perda de pacotes total: 66.82 %
Penalidade de segurança aplicada: 5000.00
Fitness final: 5116.98
Reputação de todos os nós: [62.1  1.9 15.2 50.5 86.4 82.  38.5 92.4 30.1 62.9 74.4  0.2]
Nós não confiáveis da topologia (reputação < 50): [np.int64(1), np.int64(2), np.int64(6), np.int64(8), np.int64(11)]
Nós não confiáveis presentes na rota escolhida: [np.int64(2), np.int64(6), np.int64(1), np.int64(8), np.int64(11)]

```

Considerações João e Gleice:

O primeiro laboratório, o foco esteve no acompanhamento prático das quatro etapas do Algoritmo Genético (criação, avaliação, seleção e evolução) por meio da execução do código de demonstração fornecido pelo professor, sem alterações na sua estrutura.Notou-se que a solução ótima ($x=31$, $f(x)=961$) foi identificada logo na primeira geração e mantida ao longo de todo o processo devido ao mecanismo de elitismo, que preserva o melhor indivíduo para as gerações subsequentes. Além disso, a presença contínua de indivíduos com baixo desempenho (como $x=5$ ou $x=12$) nas populações seguintes evidenciou a atuação da mutação na manutenção da diversidade do espaço de busca. Trata-se de um laboratório introdutório ("hello world" do AG) em um espaço de busca pequeno (5 bits / 32 combinações), o que viabilizou a convergência rápida para a solução ideal.