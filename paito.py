import time
import matplotlib.pyplot as plt
import networkx as nx


class grafo:

  def __init__(self,
               repr=None,
               vertices=[],
               arquivoPajek=None,
               direcionamento=False,
               ponderacao=False,
               ):
    self.repr = repr
    self.vertices = vertices
    self.ponderacao = ponderacao
    self.direcionamento = direcionamento
    self.arestas = []

    if arquivoPajek:
            self.carregarPajek(arquivoPajek)

  def salvarPajek(self, nomeArquivo):
      with open(nomeArquivo, 'w') as file:
          file.write("Representation: {}\n".format(self.repr))
          file.write("Directed: {}\n".format(self.direcionamento))
          file.write("Weighted: {}\n".format(self.ponderacao))

          file.write("*Vertices {}\n".format(len(self.vertices)))
          for i, vertice in enumerate(self.vertices, start=1):
              file.write("{} \"{}\"\n".format(i, vertice))


          if self.repr == "lista":
              file.write("*Edges\n")
              for aresta in self.arestas:
                  file.write("{} {} {}\n".format(aresta[0], aresta[1], aresta[2]))
          elif self.repr == "matriz":
              file.write("*Arcs\n")
              for i, linha in enumerate(self.matrizAdjacencia(), start=1):
                  for j, valor in enumerate(linha, start=0):
                      if valor != 0:
                          file.write("{} {} {}\n".format(i, j, valor))
          else:
              print("Representação não suportada para salvar em formato Pajek.")

      print("Grafo salvo em formato Pajek como:", nomeArquivo)

  def carregarPajek(self, nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        lines = file.readlines()

    repr = None
    vertices = []
    arestas = []
    direcionamento = False
    ponderacao = False

    for line in lines:
        if line.startswith("Representation"):
            repr = line.split(":")[1].strip()
        elif line.startswith("Directed"):
            direcionamento = line.split(":")[1].strip() == "True"
        elif line.startswith("Weighted"):
            ponderacao = line.split(":")[1].strip() == "True"
        elif line.startswith("*Vertices"):
            continue
        elif line.startswith("*Edges") or line.startswith("*Arcs"):
            if repr is None:
                repr = "lista" if line.startswith("*Edges") else "matriz"
        elif line.strip():  
            parts = line.strip().split()
            if len(parts) == 3:
                v1, v2, peso = parts
                v1 = v1.strip('"')
                v2 = v2.strip('"')
                if v1.isdigit() and v2.isdigit():
                    arestas.append((v1, v2, float(peso)))
            elif len(parts) == 2:
                v = parts[1].strip('"')
                if parts[0].isdigit():
                    vertices.append(v)

    self.repr = repr
    self.vertices = vertices
    self.ponderacao = ponderacao
    self.direcionamento = direcionamento
    self.arestas = arestas

  def prim(self, v1):
    if self.ponderacao:
      naoVisitados = self.vertices[:]
      verticeAtual = v1 
      menorDistancia = 10e9  
      mst = []
      verticeDestino = None 
      
      while naoVisitados:
        for aresta in self.arestas: 
          if aresta[0] == verticeAtual and aresta[1] in naoVisitados: 
            if aresta[2] < menorDistancia:
              menorDistancia = aresta[2]	
              verticeDestino = aresta[1]

        mst.append((verticeAtual, verticeDestino, menorDistancia))
        naoVisitados.remove(verticeAtual)
        
        verticeAtual = verticeDestino
        menorDistancia = 10e9
        verticeDestino = None

      mst.pop()

    else: 
      print("Esse grafo não é ponderado")
      
    return mst

  def gerarGrafico(self):
    eixoX = []
    eixoY = []
    degrees = []

    for vertice in self.vertices:
        degree = self.degree(vertice)
        degrees.append(degree)
        if degree not in eixoX:
            eixoX.append(degree)

    for degree in eixoX:
        y = degrees.count(degree)
        eixoY.append(y)

    plt.bar(eixoX, eixoY, color='pink', width=0.09, edgecolor='black')

    plt.xlabel('Degrees')
    plt.ylabel('Frequency')
    plt.title('Histogram')

    plt.savefig('histogram.png')
    print("Histograma salvo como PNG")
    plt.show()


  def euleriano(self, verticeInicial, verticeFinal):
    pares = []
    for vertice in self.vertices:
      degreeVertice = self.degree(vertice)
      if degreeVertice % 2 == 0:
        pares.append(vertice)

    qtdPares = len(pares)
    qtdVertices = len(self.vertices)

    if qtdPares == qtdVertices:
      print("Esse grafo é euleriano")
    elif verticeInicial not in pares and verticeFinal not in pares:
      if qtdPares == (qtdVertices - 2):
        print("Esse grafo é euleriano")
    else:
      print("Esse grafo não é euleriano")

  def buscaProfundidade(self, verticeInicial, verticeFinal):
    if self.repr == "lista":

      stack = []
      visitados = []
      stack.append(verticeInicial)

      while stack:
        verticeAtual = stack.pop()
        if verticeAtual not in visitados:
          visitados.append(verticeAtual)

        for vizinho in self.vizinhos(verticeAtual):
          if vizinho not in visitados:
            stack.append(vizinho)

        if verticeAtual == verticeFinal:
          break

      return visitados
    else:
      return "ERRO AO FAZER BUSCA EM PROFUNDIDADE: Esse grafo não é uma lista."

  def buscaLargura(self, verticeInicial, verticeFinal):
    if self.repr == "lista":
      queue = []
      visitados = []
      queue.append(verticeInicial)

      while queue:
        verticeAtual = queue.pop(0)

        if verticeAtual not in visitados:
          visitados.append(verticeAtual)

        for vizinho in self.vizinhos(verticeAtual):
          if vizinho not in visitados:
            queue.append(vizinho)

        if verticeAtual == verticeFinal:
          break

      return visitados
    else:
      return "ERRO AO FAZER BUSCA EM LARGURA: Esse grafo não é uma lista."

  def constroiMatriz(self, vertice):
    return [[0] * vertice for _ in range(vertice)]

  def copiarMatriz(self):
    self.criarMatriz()
    vertices = len(matriz)
    copia = self.constroiMatriz(vertices)

    for i in range(vertices):
      for j in range(vertices):
        copia[i][j] = matriz[i][j]

    # print("COPIA: \n", copia)
    return copia

  def warshall(self):
    matrizWarshall = self.copiarMatriz()
    # print(len(matrizWarshall)) = 4

    for k in range(len(matrizWarshall)):  # 4
      for i in range(len(matrizWarshall)):
        for j in range(len(matrizWarshall)):
          # print(j, "\n")
          matrizWarshall[i][j] = matrizWarshall[i][j] or (
              matrizWarshall[i][k] and matrizWarshall[k][j])

    return matrizWarshall

  def criarLista(self):
    global listaGrafo
    listaGrafo = {}

    # if self.repr == "lista":
    for i in range(len(self.vertices)):
        verticeAtual = self.vertices[i]

        for j in range(len(self.vertices)):
          for aresta in self.arestas:
            if aresta[0] == self.vertices[i] and aresta[1] == self.vertices[j]:
              if verticeAtual not in listaGrafo:
                listaGrafo[verticeAtual] = []
              listaGrafo[verticeAtual].append(self.vertices[j])

    return listaGrafo

    # else:
    #   print("Esse grafo não é uma lista")

  def criarMatriz(self):
    listaGrafoo = self.criarLista()
    if self.repr == "matriz":
      print('  ', end="")
      for l in range(len(self.vertices)):
        print(f"{self.vertices[l]} ", end="")
      print(end="\n")

      global matriz
      matriz = []

      for i in range(len(self.vertices)):
        linha = []
        verticeAtual = self.vertices[i]
        print(f"{self.vertices[i]} ", end="")
        for j in range(len(self.vertices)):
          achou = False
          for aresta in self.arestas:
            if aresta[0] == self.vertices[i] and aresta[1] == self.vertices[j]:
              achou = True
              print("1 ", end="")
              linha.append(1)
              if verticeAtual not in listaGrafoo:
                listaGrafoo[verticeAtual] = []
              listaGrafoo[verticeAtual].append(self.vertices[j])

          if not achou:
            print("0 ", end="")
            linha.append(0)

        matriz.append(linha)
        print(end="\n")

      # print(matriza)

    else:
      print("Esse grafo não é uma matriz")

  def outdegree(self, v1):
    global qtd_out
    qtd_out = 0
    if self.verificarVertice(v1):
      for aresta in self.arestas:
        if aresta[0] == v1:
          qtd_out += 1

    else:
      print("esse vértice não rola meu chapa")

    return qtd_out

  def indegree(self, v1):
    global qtd_in
    qtd_in = 0
    if self.verificarVertice(v1):
      for aresta in self.arestas:
        if aresta[1] == v1:
          qtd_in += 1

    else:
      print("esse vértice não rola meu chapa")
    return qtd_in

  def degree(self, v1):
    degree = self.qtdVizinhos(v1)
    return degree

  def qtdVizinhos(self, vertice):
    self.criarLista()
    vizinhos = []

    if vertice in self.vertices:
      for vizinho in listaGrafo[vertice]:
        vizinhos.append(vizinho)

    return len(vizinhos)

  def vizinhos(self, vertice):
    self.criarLista()
   
    vizinhos = []

    if vertice in self.vertices:
      for vizinho in listaGrafo[vertice]:
        vizinhos.append(vizinho)

    return vizinhos

  def adicionarVertice(self, n):
    if n in self.vertices:
      print("Esse vértice já existe nesse grafo")
    else:
      self.vertices.append(n)
      print(f"Vértice {n} adicionado com sucesso")

  def tamanhoVertices(self):
    return len(self.vertices)

  def removerAresta(self, n1, n2):
    for i in range(len(self.arestas) - 1):
      if self.arestas[i][0] == n1 and self.arestas[i][1] == n2:
        self.arestas.pop(i)
        print(f"Aresta {n1} -> {n2} removida com sucesso")
        return

    print(f"Não existe aresta entre {n1} -> {n2} ")

  def removerVertice(self, n):
    if n in self.vertices:
      self.vertices.remove(n)
      print(f"Vértice {n} removido com sucesso")

      for aresta in self.arestas[:]:
        if n in aresta:
          self.removerAresta(aresta[0], aresta[1])
    else:
      print("Esse vértice não existe nesse grafo.")

  def verificarVertice(self, v):
    if v in self.vertices:
      return True
    else:
      return False

  def atualizarPeso(self, v1, v2, novoPeso, direcionamento):
    existe = False

    for aresta in self.arestas:
      if not direcionamento:
        if (aresta[0] == v1 and aresta[1] == v2) or (aresta[0] == v2
                                                     and aresta[1] == v1):
          aresta[2] = novoPeso
          existe = True
          break
      else:
        if aresta[0] == v1 and aresta[1] == v2:
          aresta[2] = novoPeso
          existe = True
          break

    if not existe:
      if direcionamento:
        self.arestas.append([v1, v2, novoPeso])
      else:
        self.arestas.append([v1, v2, novoPeso])
        self.arestas.append([v2, v1, novoPeso])

  def adicionarAresta(self, v1, v2, peso=0, direcionado=False):
    if self.verificarVertice(v1) and self.verificarVertice(v2):
      if direcionado:
        self.arestas.append([v1, v2, peso])
      else:
        self.arestas.append([v1, v2, peso])
        self.arestas.append([v2, v1, peso])
    else:
      print("Um dos vértices não existe nesse grafo.")

  def printArestas(self):
    print("\n---- Lista de arestas: ----")
    print('   (A1 --peso-- A2)')

    for i in self.arestas:
      print(f'{i[0]} --{i[2]}--> {i[1]}')

  def verificarAresta(self, v1, v2):
    for i in range(len(self.arestas)):
      if self.arestas[i][0] == v1 and self.arestas[i][1] == v2:
        print(f"A aresta {v1} -> {v2} existe nesse grafo")
        return True
    print(f"A aresta {v1} -> {v2} não existe nesse grafo")
    return False

  def pegaPeso(self, v1, v2):
    if self.ponderacao:
      if self.verificarAresta(v1, v2):
        for aresta in self.arestas:
          if aresta[0] == v1 and aresta[1] == v2:
            print(f"O peso da aresta {v1} -> {v2} é {aresta[2]}")
            return aresta[2]
      else:
        print("Essa aresta não existe meu consagrado.")
        return None
    else:
      print("Esse grafo não é nem ponderado doido")
      return 1

  def buscaDijkstra (self, pontoInicial):
    inicio = time.time()
    naoVisitados = self.vertices.copy()
    distancias = {vertice: 10e10 for vertice in self.vertices}
    distancias[pontoInicial] = 0

    while naoVisitados:
      menorDistancia = 10e9
      proxVertice = None

      for vertice in naoVisitados:
        if distancias[vertice] < menorDistancia:
          menorDistancia = distancias[vertice]
          proxVertice = vertice

      if proxVertice is None:
        break

      naoVisitados.remove(proxVertice)

      for aresta in self.arestas:
        if aresta[0] == proxVertice:
          vizinho = aresta[1]
          peso = aresta[2]
          novaDistancia = distancias[proxVertice] + peso
          if novaDistancia < distancias[vizinho]:
            distancias[vizinho] = novaDistancia

    fim = time.time()
    tempo = fim - inicio
    print(end="\n")
    print("Tempo de busca Dijkstra: ", tempo)
    print(distancias)

  def __str__(self):

    return f"Representação: {self.repr}\nVertices: {self.vertices}\nDirecionamento: {self.direcionamento}\nPonderação: {self.ponderacao}"
