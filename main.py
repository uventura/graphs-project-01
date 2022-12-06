class Cliques:
    def __init__(self, filepath):
        self.result = []
        self.graph = self.get_graph(filepath)

    def run(self):    
        self.bron_kerbosch(list(self.graph.keys()))
        self.format_result()

    def format_result(self):
        '''
            Realiza o tratamento do resultado adquirido.
        '''
        self.result = self.remove_duplicates(self.result)
        self.result = [self.string_list_to_list(element) for element in self.result]
        self.result = self.remove_sublists(self.result)

    def remove_duplicates(self, input_list):
        '''
            Remove duplicatas de uma lista.
            Exemplo:
                lista = ['a', 'a', 'b']
                lista = remove_duplicates(lista)       # output: ['a','b']
        '''
        return list(set(input_list))

    def string_list_to_list(self, input_string):
        '''
            Faz a conversão de uma string que representa
            uma lista para o tipo de lista de propriamente.
            Exemplo:

                str_list = "['a,'b','c']"
                out_ list = string_list_to_list(str_list)   # output: ['a', 'b', 'c']
        '''
        
        output = input_string[1:-1]
        output = output.split(',')
        output = [element.strip()[1:-1] for element in output]
        return output

    def remove_sublists(self, lists):
        '''
            Remove sublistas de um dado conjunto de listas.
            Exemplo:
                L = [['a', 'b', 'c'], ['c']]
                R = remove_sublists(L) => L = [['a', 'b', 'c']]
        '''
        result = []
        analysed_list = sorted(lists, key=len)
        for i in range(len(analysed_list)):
            found = False
            for j in range(len(analysed_list) - 1, i, -1):
                if len(analysed_list[i]) == len(analysed_list[j]):
                    break
                if set(analysed_list[i]).issubset(analysed_list[j]):
                    found = True
            if not found:
                result.append(analysed_list[i])
        return result


    def decompose_line_data(self, line):
        '''
            Decompõe uma dada linha em vértices e vizinhos.

            Para cada linha presente no arquivo tem-se o seguinte aspecto:
                "país": "adversário1", "adversário2", ..., "adversárion";
            Portanto o vértice trata-se de "país" e seus vizinhos são "adversario".
        '''

        data_line = line.split(':')
        vertex = data_line[0]
        neighbours = sorted([data.strip()[:-1] for data in data_line[1].split()])

        return [vertex, neighbours]

    def get_graph(self, filepath):
        ''''
            Constrói um grafo a partir de um dado arquivo.
        '''

        graph_file = open(filepath, 'r')
        file_lines = graph_file.readlines()

        graph = {}
        for line in file_lines:
            if line[0] not in ['%', '\n']:
                node = self.decompose_line_data(line)
                graph[node[0]] = node[1]

        return graph

    def intersection(self, a, b):
        '''
            Realiza a interceção entre dois elementos.
            Exemplo:
                A = [a, b, c]
                B = [b]
                C = intercetion(a, b) # => [b]
        '''

        result = []
        for element in a:
            if element in b:
                result.append(element)

        return result

    def bron_kerbosch(self, P, R = [], X = []):
        print(f'P = {P}, R = {R}, X = {X}')

        if len(P) + len(X) == 0:
            self.result.append(str(sorted(R)))

        # Índice do vértice analisado
        vertex_index = 0
        while len(P) != 0:
            # Vértice atual
            vertex = P[vertex_index]

            # Vizinhos dos vértice
            neighbours = self.graph[vertex]

            # Intercecção entre P e os vizinhos do vértice
            new_P = self.intersection(P, neighbours)
            # União de R e vértice
            new_R = R + [vertex]
            # Intercecção entre X e os vizinhos do vértice
            new_X = self.intersection(X, neighbours)

            # Aplicação recursiva
            self.bron_kerbosch(new_P, new_R, new_X)

            # Remove vértice de P
            P.remove(vertex)
            # Acresenta vértice a X
            X.append(vertex)

        return

    def get_maximum(self):
        maximum = {}
        for index, element in enumerate(self.result):
            if len(element) in maximum:
                maximum[len(element)].append(index)
            else:
                maximum[len(element)] = [index]
        max_elements = maximum[max(maximum.keys())]
        maximum = [self.result[element] for element in max_elements]
        return maximum

    def common_neighbours(self, vertex_a):
        '''
            Verifica os vizinhos em comuns de vértices
            vizinhos em um grafo.
        '''

        combinations = []
        for neighbour in self.graph[vertex_a]:
            for another_neighbour in self.graph[vertex_a]:
                if another_neighbour in self.graph[neighbour] \
                and another_neighbour != neighbour \
                and {vertex_a, neighbour, another_neighbour} not in combinations:
                    combinations.append({vertex_a, neighbour, another_neighbour})
        return len(combinations)

    def aglomeration_coeficient(self):
        '''
            Coeficiente de aglomeração médio.
        '''

        C = 0
        for element in list(self.graph.keys()):
            if len(self.graph[element]) < 2:
                continue

            ci = self.common_neighbours(element)
            ci = 2 * ci / (len(self.graph[element]) * (len(self.graph[element]) - 1))
            C += ci
        return float(C/float(len(self.graph.keys())))

if __name__ == '__main__':
    cliques = Cliques("cliques_copas.txt")

    print("="*10)
    print("Cálculos intermediários:\n")
    cliques.run()

    print("="*10)
    print("Cliques acima de 3:\n")
    for result in cliques.result[::-1]:
        if len(result) > 3:
            print(f'Vertices = {len(result)}, Conjunto = {result}')

    print("="*10)
    print("Maximos:\n")
    for result in cliques.get_maximum():
        print(f'Vertices = {len(result)}, Conjunto = {result}')

    print("="*10)
    print(f"Coeficiente de Aglomeracao Medio = {cliques.aglomeration_coeficient()}\n")
