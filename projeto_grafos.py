from queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt 

roteadores = dict() #Dicionário que irá armazenar os roteadores


# Abre o arquivo que contém os dados da rede
with open("dadaset_redes.txt", "r") as arquivo:
    # Lê o arquivo linha por linha até o fim
    while True: 
        linha = arquivo.readline()

        # Verifica se ainda existe conteúdo
        if linha: 
            # Divide a linha em duas partes usando ":"
            divisao = linha.split(":")
            node = divisao[0].strip()   # Obtém o nome do roteador pegando o índice 0 e removendo espaço vazio

            # Armazena no dicionário as conexões 
            roteadores[node] = eval(divisao[1].strip())
        else:
            break

# Definição das funções de Busca Uniforme e Algoritmo Djikstra

def BuscaUniforme(grafo,inicio,alvo):
    fila = PriorityQueue()  
    visitados = set()   

    # Insere o nó inicial na fila
    fila.put((0,inicio,[inicio]))

    # Continua enquanto houver elementos na fila
    while not fila.empty():

        custoAtual, roteadorAtual, caminho = fila.get()

        # Ignora caso o nó já tenha sido visitado
        if roteadorAtual in visitados:
            continue
        
        # Marca o nó como visitado
        visitados.add(roteadorAtual)

        # Se encontrou o destino retorna o custo e o caminho percorrido
        if roteadorAtual == alvo:
            return custoAtual, caminho
        
        # Percorre os vizinhos do nó atual
        for vizinho, custoVizinho in grafo[roteadorAtual]:
            # Se o vizinho não foi vistado
            if vizinho not in visitados:    
                novoCusto = custoAtual + custoVizinho
                novoCaminho = caminho + [vizinho]
                # Adiciona na fila o novo custo, e o caminho atualizado
                fila.put((novoCusto,vizinho,novoCaminho))

    return "Alvo não encontrado"    

def AlgoritmoDjikstra(grafo, inicio):
    fila = PriorityQueue()  
    menoresDistancias = dict()  # Armazena menor distância encontrada para cada nó do grafo
    ancestrais = dict() # Como se fosse uma corrente 

    # Inicializa todas as distâncias com infinito e que não tem nenhum nó com ancestral
    for roteador in grafo:
        menoresDistancias[roteador] = float("inf")
        ancestrais[roteador] = None

    menoresDistancias[inicio] = 0

    # Adiciona o nó inicial na fila
    fila.put((0,inicio))

    while not fila.empty():
        custoAtual, roteadorAtual = fila.get()

        if custoAtual > menoresDistancias[roteadorAtual]:
            continue
        
        for vizinho, custoVizinho in grafo[roteadorAtual]:
            novoCusto = custoAtual + custoVizinho

            # Se encontrou um caminho melhor
            if novoCusto < menoresDistancias[vizinho]:

                # Atualizar a menor distância
                menoresDistancias[vizinho] = novoCusto
                ancestrais[vizinho] = roteadorAtual   # Atualiza o ancestral

                fila.put((novoCusto,vizinho))   # Insere o vizinho na fila com o novo custo
    return menoresDistancias, ancestrais    # Retorna as menores distâncias e os ancestrais para cada nó do grafo

def ArvoreDijkstra(ancestrais):
    arestasArvore = []  # Armazena as arestas da árvore de Dijkstra

    for roteador, ancestral in ancestrais.items():
        if ancestral:   # Se existir um ancestral, cria a aresta entre o roteador e seu ancestral
            arestasArvore.append((roteador,ancestral))

    return arestasArvore    # Retorna todas as arestas 

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


# 1.  Qual é a menor latência entre CORE001 e cada um dos 200 roteadores da rede?
print("\n1. Qual é a menor latência entre CORE001 e cada um dos 200 roteadores da rede?")
for roteador, distancia in distancias.items():
    print(f"{roteador}: {distancia}ms")
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

plt.figure(figsize=(24, 16))
pos = nx.bfs_layout(grafo,origem)

nx.draw_networkx_edges(grafo,pos,width=0.6)
nx.draw_networkx_edges(grafo,pos,edge_color="red",edgelist=arestas,width=3.5)

nx.draw_networkx_nodes(grafo,pos,node_size=200)
nx.draw_networkx_nodes(grafo,pos,node_color="orange",nodelist=[origem],node_size=800)
nx.draw_networkx_nodes(grafo,pos,node_color="red",nodelist=list(nos_arvore),node_size=350)

nx.draw_networkx_labels(grafo,pos,font_size=6)
peso = nx.get_edge_attributes(grafo,"weight")
nx.draw_networkx_edge_labels(grafo,pos,edge_labels=peso,font_size=6)

plt.title(f"Grafo produzido pelo algoritmo de Dijkstra a partir de {origem}",fontsize=15)
plt.show()
