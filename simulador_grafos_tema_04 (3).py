from collections import deque
import heapq

ARISTAS = [
    ('A', 'B', 2), ('A', 'C', 5), ('A', 'G', 15),
    ('B', 'C', 1), ('B', 'D', 2), ('C', 'E', 3),
    ('C', 'G', 12), ('D', 'E', 1), ('D', 'F', 6),
    ('E', 'F', 2), ('F', 'G', 1), ('G', 'E', 4),
    ('G', 'H', 2),
]
NODOS = tuple('ABCDEFGH')

def construir_grafo(aristas=ARISTAS):
    grafo = {v: {} for v in NODOS}
    for u, v, peso in aristas:
        if peso < 0:
            raise ValueError('Dijkstra requiere pesos no negativos')
        grafo[u][v] = peso
    return grafo

def reconstruir(padres, origen, destino):
    if destino not in padres:
        return None
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padres[actual]
    camino.reverse()
    return camino if camino[0] == origen else None

def bfs(grafo, origen, destino):
    cola = deque([origen]); padres = {origen: None}; orden = []
    while cola:
        u = cola.popleft(); orden.append(u)
        if u == destino:
            break
        for v in sorted(grafo[u]):
            if v not in padres:
                padres[v] = u; cola.append(v)
    return reconstruir(padres, origen, destino), orden

def dfs_alcanzables(grafo, origen):
    vistos = set(); orden = []; pila = [origen]
    while pila:
        u = pila.pop()
        if u in vistos:
            continue
        vistos.add(u); orden.append(u)
        pila.extend(sorted(grafo[u], reverse=True))
    return orden

def dijkstra(grafo, origen, destino):
    distancia = {v: float('inf') for v in grafo}
    padres = {origen: None}
    distancia[origen] = 0
    monticulo = [(0, origen)]
    while monticulo:
        d, u = heapq.heappop(monticulo)
        if d != distancia[u]:
            continue
        if u == destino:
            break
        for v, peso in sorted(grafo[u].items()):
            candidato = d + peso
            if candidato < distancia[v]:
                distancia[v] = candidato
                padres[v] = u
                heapq.heappush(monticulo, (candidato, v))
    if distancia[destino] == float('inf'):
        return None, None
    return reconstruir(padres, origen, destino), distancia[destino]

def componentes_fuertemente_conexas(grafo):
    visitados = set(); finalizacion = []

    def visita(u):
        visitados.add(u)
        for v in sorted(grafo[u]):
            if v not in visitados:
                visita(v)
        finalizacion.append(u)

    for u in sorted(grafo):
        if u not in visitados:
            visita(u)
    transpuesto = {u: [] for u in grafo}
    for u in grafo:
        for v in grafo[u]:
            transpuesto[v].append(u)
    visitados.clear(); componentes = []

    def recoger(u, grupo):
        visitados.add(u); grupo.append(u)
        for v in sorted(transpuesto[u]):
            if v not in visitados:
                recoger(v, grupo)

    for u in reversed(finalizacion):
        if u not in visitados:
            grupo = []
            recoger(u, grupo)
            componentes.append(tuple(sorted(grupo)))
    return sorted(componentes, key=lambda c: c[0])

def sin_arista(grafo, origen, destino):
    copia = {u: dict(adyacentes) for u, adyacentes in grafo.items()}
    copia[origen].pop(destino, None)
    return copia

def ejecutar():
    base = construir_grafo()
    camino_bfs, orden_bfs = bfs(base, 'A', 'H')
    camino_min, costo = dijkstra(base, 'A', 'H')
    assert camino_bfs == ['A', 'G', 'H']
    assert camino_min == ['A', 'B', 'D', 'E', 'F', 'G', 'H'] and costo == 10
    assert len(dfs_alcanzables(base, 'A')) == 8
    assert len(dfs_alcanzables(base, 'H')) == 1
    assert len(componentes_fuertemente_conexas(base)) == 6
    assert ('E', 'F', 'G') in componentes_fuertemente_conexas(base)

    casos = [('Base', base),
            ('Sin B->D', sin_arista(base, 'B', 'D')),
            ('Sin E->F', sin_arista(base, 'E', 'F')),
            ('Sin G->H', sin_arista(base, 'G', 'H'))]
    print('ESCENARIO | RUTA A-H | COSTO | ALCANZABLES A | CFC')
    for nombre, grafo in casos:
        camino, valor = dijkstra(grafo, 'A', 'H')
        alcance = len(dfs_alcanzables(grafo, 'A'))
        cfc = len(componentes_fuertemente_conexas(grafo))
        print(f'{nombre} | {"->".join(camino) if camino else "Sin ruta"} | '
            f'{valor if valor is not None else "N/A"} | {alcance} | {cfc}')
    assert dijkstra(casos[1][1], 'A', 'H')[1] == 11
    assert dijkstra(casos[2][1], 'A', 'H')[1] == 13
    assert dijkstra(casos[3][1], 'A', 'H') == (None, None)
    print('BFS A-H:', '->'.join(camino_bfs), '| aristas:', len(camino_bfs)-1)
    print('Dijkstra A-H:', '->'.join(camino_min), '| minutos:', costo)
    print('DFS desde A:', ', '.join(dfs_alcanzables(base, 'A')))
    print('CFC base:', componentes_fuertemente_conexas(base))
    print('Pruebas de aserción: satisfactorias.')

if __name__ == '__main__':
    ejecutar()
