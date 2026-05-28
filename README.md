# 8-Puzzle Solver

Solução completa para o problema do **8-puzzle** implementada em Python puro, com sete algoritmos de busca e interface CLI interativa. Desenvolvida como Atividade Prática #2 da disciplina de Inteligência Artificial — PUC Minas, Campus Lourdes.

## Pré-requisitos

- Python 3.8 ou superior
- Nenhuma dependência externa — apenas biblioteca padrão

---

## Como executar

Clone o repositório e rode diretamente:

```bash
git clone https://github.com/seu-usuario/8-puzzle-solver.git
cd 8-puzzle-solver
python puzzle.py
```

O programa pergunta o estado inicial, exibe os estados objetivo e inicial, e oferece duas opções: rodar todos os algoritmos de uma vez (com tabela comparativa) ou escolher um algoritmo específico.

## Saída por execução

Para cada algoritmo, o programa exibe:

- Caminho completo de movimentos (UP / DOWN / LEFT / RIGHT)
- Número de nós visitados e gerados
- Profundidade da solução (número de movimentos)
- Tempo de execução em milissegundos
- Tabuleiro passo a passo

Ao rodar todos os algoritmos, uma **tabela comparativa** é exibida ao final.

---

## Resultados experimentais

Instância difícil: `8 1 3 4 0 2 7 6 5` (profundidade ótima = 22)

| Algoritmo | Tempo (ms) | Nós visitados | Profundidade |
|---|---|---|---|
| BFS | 198 | 75.144 | 22 |
| DFS | 87 | 52.480 | 46 |
| Custo Uniforme | 424 | 81.752 | 22 |
| Gulosa | 2 | 283 | 108 |
| A\* Peças fora do lugar | 60 | 9.965 | 22 |
| A\* Manhattan | 11 | 1.372 | 22 |
| A\* Conflito Linear | 22 | 765 | 22 |

O A\* com Manhattan é **55× mais rápido** que o BFS e visita **98% menos nós** na instância difícil, mantendo a otimalidade da solução.

---

## Estrutura do código

```
puzzle.py
├── Representação do estado      # tupla plana de 9 inteiros; 0 = espaço vazio
├── get_successors()             # geração dos estados filhos (UP/DOWN/LEFT/RIGHT)
├── is_solvable()                # verificação por contagem de inversões
├── h_misplaced()                # heurística H1
├── h_manhattan()                # heurística H2
├── h_linear_conflict()          # heurística H3
├── astar() / bfs() / dfs()
│   ucs() / greedy()             # algoritmos de busca
├── reconstruct()                # reconstrução do caminho via came_from
└── main() / run_all()           # interface CLI
```

O código é **completamente modular**: as funções de heurística, geração de sucessores e algoritmos são independentes e reutilizáveis.

---

## Heurísticas do A\*

**H1 — Peças fora do lugar:** conta quantas peças não estão na posição objetivo. Admissível pois cada peça deslocada exige ao menos 1 movimento.

**H2 — Distância de Manhattan:** soma das distâncias horizontais + verticais de cada peça até sua posição objetivo. Admissível e domina H1 (H2 ≥ H1 para todo estado).

**H3 — Conflito linear:** H2 + 2 por cada par de peças na mesma linha/coluna objetivo mas em ordem invertida. Admissível e domina H2 (H3 ≥ H2 para todo estado).

---

## Detecção de estados insolúveis

Antes de qualquer busca, o programa verifica a **paridade das inversões**: uma configuração é solúvel se e somente se o número de inversões na permutação (excluindo o zero) for par. Estados insolúveis são detectados imediatamente sem consumir recursos de busca.

---

## Disciplina

Atividade Prática #2 — Algoritmos de Busca no Jogo 8-Puzzle  
Disciplina: Inteligência Artificial  
Curso: Ciência da Computação — PUC Minas, Campus Lourdes  
Entrega: 26/06/2026
