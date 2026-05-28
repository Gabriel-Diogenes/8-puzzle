"""
8-Puzzle Solver — Atividade Prática #2
Algoritmos de Busca: A* (3 heurísticas), BFS, DFS, Custo Uniforme, Gulosa
"""
import heapq
import time
from collections import deque
from copy import deepcopy

OBJETIVO = (0, 1, 2,
        3, 4, 5,
        6, 7, 8)

def para_tupla(tabuleiro):
    """Converte lista 3x3 ou plana em tupla plana."""
    if isinstance(tabuleiro[0], (list, tuple)):
        return tuple(x for row in tabuleiro for x in row)
    return tuple(tabuleiro)

def para_grade(estado):
    """Converte tupla plana para lista 3x3."""
    return [list(estado[i*3:(i+1)*3]) for i in range(3)]

def encontrar_vazio(estado):
    return estado.index(0)

MOVES = {
    'CIMA':      -3,
    'BAIXO':     +3,
    'ESQUERDA':  -1,
    'DIREITA':   +1,
}

def obter_sucessores(estado):
    """Retorna lista de (novo_estado, acao)."""
    vazio = encontrar_vazio(estado)
    linha, coluna = divmod(vazio, 3)
    sucessores = []
    for acao, delta in MOVES.items():
        novo_indice = vazio + delta
        if acao == 'CIMA' and linha == 0: continue
        if acao == 'BAIXO' and linha == 2: continue
        if acao == 'ESQUERDA' and coluna == 0: continue
        if acao == 'DIREITA' and coluna == 2: continue
        lst = list(estado)
        lst[vazio], lst[novo_indice] = lst[novo_indice], lst[vazio]
        sucessores.append((tuple(lst), acao))
    return sucessores


def eh_soluvel(estado):
    """Conta inversões; par → solúvel."""
    pecas = [x for x in estado if x != 0]
    inversoes = sum(1 for i in range(len(pecas))
                    for j in range(i+1, len(pecas))
                    if pecas[i] > pecas[j])
    return inversoes % 2 == 0


def h_fora_do_lugar(estado):
    """H1 — Peças fora do lugar (admissível)."""
    return sum(1 for i, v in enumerate(estado) if v != 0 and v != OBJETIVO[i])


def h_manhattan(estado):
    """H2 — Distância de Manhattan (admissível, dominante sobre H1)."""
    total = 0
    for i, v in enumerate(estado):
        if v == 0:
            continue
        objetivo_linha, objetivo_coluna = divmod(OBJETIVO.index(v), 3)
        linha, coluna = divmod(i, 3)
        total += abs(objetivo_linha - linha) + abs(objetivo_coluna - coluna)
    return total


def h_conflito_linear(estado):
    """H3 — Manhattan + conflito linear (admissível, dominante sobre H2)."""
    base = h_manhattan(estado)
    conflitos = 0
    grade = para_grade(estado)

    for linha in range(3):
        for c1 in range(3):
            for c2 in range(c1 + 1, 3):
                v1, v2 = grade[linha][c1], grade[linha][c2]
                if v1 == 0 or v2 == 0: continue
                objetivo_linha_v1 = OBJETIVO.index(v1) // 3
                objetivo_linha_v2 = OBJETIVO.index(v2) // 3
                objetivo_coluna_v1 = OBJETIVO.index(v1) % 3
                objetivo_coluna_v2 = OBJETIVO.index(v2) % 3
                if objetivo_linha_v1 == linha and objetivo_linha_v2 == linha and objetivo_coluna_v1 > objetivo_coluna_v2:
                    conflitos += 2

    for coluna in range(3):
        for l1 in range(3):
            for l2 in range(l1 + 1, 3):
                v1, v2 = grade[l1][coluna], grade[l2][coluna]
                if v1 == 0 or v2 == 0: continue
                objetivo_coluna_v1 = OBJETIVO.index(v1) % 3
                objetivo_coluna_v2 = OBJETIVO.index(v2) % 3
                objetivo_linha_v1 = OBJETIVO.index(v1) // 3
                objetivo_linha_v2 = OBJETIVO.index(v2) // 3
                if objetivo_coluna_v1 == coluna and objetivo_coluna_v2 == coluna and objetivo_linha_v1 > objetivo_linha_v2:
                    conflitos += 2

    return base + conflitos


HEURISTICS = {
    'fora_do_lugar':       h_fora_do_lugar,
    'manhattan':           h_manhattan,
    'conflito_linear':     h_conflito_linear,
}


def reconstruir(vem_de, estado):
    caminho, acoes = [], []
    while vem_de[estado] is not None:
        pai, acao = vem_de[estado]
        caminho.append(estado)
        acoes.append(acao)
        estado = pai
    caminho.append(estado)
    caminho.reverse(); acoes.reverse()
    return caminho, acoes


def a_estrela(inicio, heuristica_fn):
    tempo_inicio = time.time()
    h0 = heuristica_fn(inicio)
    fila = [(h0, 0, inicio)]
    vem_de = {inicio: None}
    custo_g = {inicio: 0}
    visitados = 0

    while fila:
        f, g, estado = heapq.heappop(fila)
        visitados += 1

        if estado == OBJETIVO:
            caminho, acoes = reconstruir(vem_de, estado)
            return {
                'found': True,
                'path': caminho,
                'actions': acoes,
                'visited': visitados,
                'depth': len(acoes),
                'time': time.time() - tempo_inicio,
                'generated': len(vem_de),
            }

        for proximo_estado, acao in obter_sucessores(estado):
            novo_g = g + 1
            if proximo_estado not in custo_g or novo_g < custo_g[proximo_estado]:
                custo_g[proximo_estado] = novo_g
                vem_de[proximo_estado] = (estado, acao)
                heapq.heappush(fila, (novo_g + heuristica_fn(proximo_estado), novo_g, proximo_estado))

    return {'found': False, 'visited': visitados, 'time': time.time() - tempo_inicio}


def busca_largura(inicio):
    tempo_inicio = time.time()
    if inicio == OBJETIVO:
        return {'found': True, 'path': [inicio], 'actions': [], 'visited': 1, 'depth': 0, 'time': 0, 'generated': 1}
    fila = deque([inicio])
    vem_de = {inicio: None}
    visitados = 0

    while fila:
        estado = fila.popleft()
        visitados += 1
        for proximo_estado, acao in obter_sucessores(estado):
            if proximo_estado not in vem_de:
                vem_de[proximo_estado] = (estado, acao)
                if proximo_estado == OBJETIVO:
                    caminho, acoes = reconstruir(vem_de, proximo_estado)
                    return {
                        'found': True,
                        'path': caminho, 'actions': acoes,
                        'visited': visitados, 'depth': len(acoes),
                        'time': time.time() - tempo_inicio, 'generated': len(vem_de),
                    }
                fila.append(proximo_estado)

    return {'found': False, 'visited': visitados, 'time': time.time() - tempo_inicio}


def busca_profundidade(inicio, limite_profundidade=50):
    tempo_inicio = time.time()
    pilha = [(inicio, None, None, 0)]
    vem_de = {inicio: None}
    visitados = 0
    gerados = 1

    while pilha:
        estado, pai, acao, profundidade = pilha.pop()
        visitados += 1

        if estado == OBJETIVO:
            caminho, acoes = [estado], [acao] if acao else []
            atual = pai
            while atual is not None and atual in vem_de:
                anterior = vem_de.get(atual)
                caminho.append(atual)
                if anterior and anterior[1]:
                    acoes.append(anterior[1])
                atual = anterior[0] if anterior else None
            caminho.reverse(); acoes.reverse()
            return {
                'found': True,
                'path': caminho, 'actions': acoes,
                'visited': visitados,
                'depth': profundidade,
                'time': time.time() - tempo_inicio, 'generated': gerados,
            }

        if profundidade >= limite_profundidade:
            continue

        for proximo_estado, proxima_acao in obter_sucessores(estado):
            if proximo_estado not in vem_de:
                vem_de[proximo_estado] = (estado, proxima_acao)
                pilha.append((proximo_estado, estado, proxima_acao, profundidade + 1))
                gerados += 1

    return {'found': False, 'visited': visitados, 'time': time.time() - tempo_inicio}


def custo_uniforme(inicio):
    tempo_inicio = time.time()
    fila_prioridade = [(0, inicio)]
    vem_de = {inicio: None}
    custo = {inicio: 0}
    visitados = 0

    while fila_prioridade:
        g, estado = heapq.heappop(fila_prioridade)
        visitados += 1

        if estado == OBJETIVO:
            caminho, acoes = reconstruir(vem_de, estado)
            return {
                'found': True,
                'path': caminho, 'actions': acoes,
                'visited': visitados,
                'depth': len(acoes),
                'time': time.time() - tempo_inicio,
                'generated': len(vem_de),
            }

        for proximo_estado, acao in obter_sucessores(estado):
            novo_g = g + 1
            if proximo_estado not in custo or novo_g < custo[proximo_estado]:
                custo[proximo_estado] = novo_g
                vem_de[proximo_estado] = (estado, acao)
                heapq.heappush(fila_prioridade, (novo_g, proximo_estado))

    return {'found': False, 'visited': visitados, 'time': time.time() - tempo_inicio}


def gulosa(inicio, heuristica_fn=h_manhattan):
    tempo_inicio = time.time()
    fila_prioridade = [(heuristica_fn(inicio), inicio)]
    vem_de = {inicio: None}
    visitados = 0

    while fila_prioridade:
        _, estado = heapq.heappop(fila_prioridade)
        visitados += 1

        if estado == OBJETIVO:
            caminho, acoes = reconstruir(vem_de, estado)
            return {
                'found': True,
                'path': caminho,
                'actions': acoes,
                'visited': visitados,
                'depth': len(acoes),
                'time': time.time() - tempo_inicio,
                'generated': len(vem_de),
            }

        for proximo_estado, acao in obter_sucessores(estado):
            if proximo_estado not in vem_de:
                vem_de[proximo_estado] = (estado, acao)
                heapq.heappush(fila_prioridade, (heuristica_fn(proximo_estado), proximo_estado))

    return {'found': False, 'visited': visitados, 'time': time.time() - tempo_inicio}


def imprimir_tabuleiro(estado):
    simbolos = {0: ' '}
    for i in range(3):
        linha = estado[i*3:(i+1)*3]
        print('+---+---+---+')
        print('| ' + ' | '.join(simbolos.get(v, str(v)) for v in linha) + ' |')
    print('+---+---+---+')


def imprimir_resultado(res, nome_algo):
    print(f"  {nome_algo}")
    if not res['found']:
        print("  ✗ Solução NÃO encontrada.")
    else:
        print(f"  Profundidade      : {res['depth']}")
        print(f"  Nós visitados     : {res['visited']}")
        print(f"  Nós gerados       : {res.get('generated', '-')}")
        print(f"  Tempo de execução : {res['time']*1000:.2f} ms")
        print(f"\n  Movimentos ({len(res['actions'])}): {' → '.join(res['actions'])}")
        print("\n  Caminho passo a passo:")
        for passo, estado in enumerate(res['path']):
            print(f"\n  Passo {passo}:")
            print('  +---+---+---+')
            for i in range(3):
                linha = estado[i*3:(i+1)*3]
                print('  | ' + ' | '.join(' ' if v == 0 else str(v) for v in linha) + ' |')
            print('  +---+---+---+')


def executar_todos(inicio):
    """Executa todos os algoritmos e retorna resultados."""
    if not eh_soluvel(inicio):
        print("\nEstado inicial NÃO tem solução (número ímpar de inversões).")
        return

    resultados = {}
    algoritmos = [
        ('BFS',                    lambda: busca_largura(inicio)),
        ('DFS',                    lambda: busca_profundidade(inicio)),
        ('Custo Uniforme',         lambda: custo_uniforme(inicio)),
        ('Gulosa (Manhattan)',      lambda: gulosa(inicio, h_manhattan)),
        ('A* — Peças Fora do Lugar', lambda: a_estrela(inicio, h_fora_do_lugar)),
        ('A* — Manhattan',         lambda: a_estrela(inicio, h_manhattan)),
        ('A* — Conflito Linear',   lambda: a_estrela(inicio, h_conflito_linear)),
    ]
    for nome, fn in algoritmos:
        res = fn()
        resultados[nome] = res
        imprimir_resultado(res, nome)

    # Tabela comparativa
    print(f"\n{'='*65}")
    print(f"  TABELA COMPARATIVA")
    print(f"{'='*65}")
    print(f"{'Algoritmo':<30} {'Tempo(ms)':>10} {'Visitados':>10} {'Profund.':>9}")
    print(f"{'-'*65}")
    for nome, res in resultados.items():
        if res['found']:
            t = f"{res['time']*1000:.2f}"
            print(f"{nome:<30} {t:>10} {res['visited']:>10} {res['depth']:>9}")
        else:
            print(f"{nome:<30} {'—':>10} {res['visited']:>10} {'N/A':>9}")
    print(f"{'='*65}")
    return resultados


def principal():
    print("         8-Puzzle Solver           ")
    print("\nInsira o estado inicial como 9 números separados por espaço.")
    print("Use 0 para o espaço vazio. Ex: 1 2 5 3 4 0 6 7 8\n")

    while True:
        entrada_bruta = input("Estado inicial: ").strip()
        try:
            numeros = list(map(int, entrada_bruta.split()))
            if sorted(numeros) != list(range(9)):
                print("Erro: use exatamente os números 0-8 sem repetição.")
                continue
            break
        except ValueError:
            print("Erro: entrada inválida.")

    inicio = tuple(numeros)
    print("\nEstado inicial:")
    imprimir_tabuleiro(inicio)
    print("\nEstado objetivo:")
    imprimir_tabuleiro(OBJETIVO)

    print("\nDeseja executar todos os algoritmos? (s/n)")
    escolha = input("> ").strip().lower()
    if escolha == 's':
        executar_todos(inicio)
    else:
        print("\nAlgoritmos disponíveis:")
        menu = [
            "BFS",
            "DFS",
            "Custo Uniforme (UCS)",
            "Gulosa (Greedy)",
            "A* — Peças Fora do Lugar",
            "A* — Manhattan",
            "A* — Conflito Linear",
        ]
        for i, m in enumerate(menu, 1):
            print(f"  {i}. {m}")
        idx = int(input("\nEscolha: ")) - 1
        funcoes = [
            lambda: busca_largura(inicio),
            lambda: busca_profundidade(inicio),
            lambda: custo_uniforme(inicio),
            lambda: gulosa(inicio),
            lambda: a_estrela(inicio, h_fora_do_lugar),
            lambda: a_estrela(inicio, h_manhattan),
            lambda: a_estrela(inicio, h_conflito_linear),
        ]
        res = funcoes[idx]()
        imprimir_resultado(res, menu[idx])

if __name__ == '__main__':
    principal()
