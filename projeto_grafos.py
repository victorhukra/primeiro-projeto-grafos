from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt

roteadores = dict()

with open("dadaset_redes.txt", "r") as arquivo:
    while True:
        linha = arquivo.readline()
        if linha: 
            divisao = linha.split(":")
            node = divisao[0].strip()

            roteadores[node] = eval(divisao[1].strip())
        else:
            break

# Definição das funções de Busca Uniforme e Algoritmo Djikstra

def BuscaUniforme(grafo,inicio,alvo):
    fila = PriorityQueue()
    visitados = set()

    fila.put((0,inicio,[inicio]))

    while not fila.empty():
        custoAtual, cidadeAtual, caminho = fila.get()

        if cidadeAtual in visitados:
            continue

        visitados.add(cidadeAtual)

        if cidadeAtual == alvo:
            return custoAtual, caminho
        
        for vizinho, custoVizinho in grafo[cidadeAtual]:
            if vizinho not in visitados:
                novoCusto = custoAtual + custoVizinho
                novoCaminho = caminho + [vizinho]

                fila.put((novoCusto,vizinho,novoCaminho))

    return "Alvo não encontrado"

def AlgoritmoDjikstra(grafo, inicio):
    fila = PriorityQueue()
    menoresDistancias = dict()
    ancestrais = dict()

    for cidade in grafo:
        menoresDistancias[cidade] = float("inf")
        ancestrais[cidade] = None

    menoresDistancias[inicio] = 0

    fila.put((0,inicio))

    while not fila.empty():
        custoAtual, cidadeAtual = fila.get()

        if custoAtual > menoresDistancias[cidadeAtual]:
            continue

        for vizinho, custoVizinho in grafo[cidadeAtual]:
            novoCusto = custoAtual + custoVizinho

            if novoCusto < menoresDistancias[vizinho]:
                menoresDistancias[vizinho] = novoCusto
                ancestrais[vizinho] = cidadeAtual

                fila.put((novoCusto,vizinho))
    return menoresDistancias, ancestrais

def ArvoreDijkstra(ancestrais):
    arestasArvore = []

    for cidade, ancestral in ancestrais.items():
        if ancestral:
            arestasArvore.append((cidade,ancestral))

    return arestasArvore

# Problema 1 
print("\n----- Problema 1 -----")

origem = "CORE001"
alvo = "IOT045"

custo, caminho = BuscaUniforme(roteadores,origem,alvo)

# 1.  Qual é o caminho de menor latência entre CORE001 e IOT045? 
print("\n1.  Qual é o caminho de menor latência entre CORE001 e IOT045?\nO caminho de menor latência percorre o seguinte trajeto: ", " -> ".join(str(n) for n in caminho))
# 2.  Qual é a latência total da rota encontrada? 
print("\n2.  Qual é a latência total da rota encontrada?\nA latência total encontrada foi", custo)
# 3.  Quantos roteadores foram percorridos? 
print(f"\n3.  Quantos roteadores foram percorridos?\nForam percorridos {len(caminho)} roteadores")

# Problema 2
print("\n----- Problema 2 -----")

distancias, ancestrais = AlgoritmoDjikstra(roteadores,origem)

for r,d in distancias.items():
    print(r,d)
# 1.  Qual é a menor latência entre CORE001 e cada um dos 200 roteadores da rede?
print(f"\n1.  Qual é a menor latência entre CORE001 e cada um dos 200 roteadores da rede?\nA menor latência em relação ao servidor central foi {min(dist for dist in distancias.values() if dist>0)} ") 
# 2.  Qual roteador apresenta a maior latência em relação ao servidor central? 
print(f"\n2.  Qual roteador apresenta a maior latência em relação ao servidor central?\nO roteador de maior latência em relação ao servidor central foi {max(distancias)}")
# 3.  Qual é a latência média da rede? 
print(f"\n3.  Qual é a latência média da rede?\nA latência média encontrada foi {sum(distancias.values())/len(distancias)}")
# 4.  Plote o grafo original e destaque, em outra cor, as arestas pertencentes à árvore produzida pelo Dijkstra. 
print("\n4.  Plote o grafo original e destaque, em outra cor, as arestas pertencentes à árvore produzida pelo Dijkstra.")

arestas = ArvoreDijkstra(ancestrais)

nos_arvore = set()

for origem_aresta, destino_aresta in arestas:
    nos_arvore.add(origem_aresta)
    nos_arvore.add(destino_aresta)

grafo = nx.Graph()

for roteador, vizinhos in roteadores.items():
    for vizinho, custo in vizinhos:
        grafo.add_edge(roteador,vizinho,weight=custo)

plt.figure(figsize=(50,25))
pos = nx.bfs_layout(grafo,origem)

nx.draw_networkx_edges(grafo,pos,width=1)
nx.draw_networkx_edges(grafo,pos,edge_color="red",edgelist=arestas,width=2)

nx.draw_networkx_nodes(grafo,pos,node_size=500)
nx.draw_networkx_nodes(grafo,pos,node_color="orange",nodelist=[origem],node_size=1000)
nx.draw_networkx_nodes(grafo,pos,node_color="red",nodelist=list(nos_arvore),node_size=500)

nx.draw_networkx_labels(grafo,pos)
peso = nx.get_edge_attributes(grafo,"weight")
nx.draw_networkx_edge_labels(grafo,pos,edge_labels=peso,font_size=10)

plt.title(f"Grafo produzido pelo algoritmo de Dijkstra a partir de {origem}",fontsize=15)
plt.show()
