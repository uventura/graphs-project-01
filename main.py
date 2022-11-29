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
        self.result = sorted(self.result, key=len, reverse=True)

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

    def decompose_line_data(self, line):
        '''
            Decompõe uma dada linha em vértices e vizinhos.

            Para cada linha presente no arquivo tem-se o seguinte aspecto:
                "país": "adversário1", "adversário2", ..., "adversárion";
            Portanto o vértice trata-se de "país" e seus vizinhos são "adversario".
        '''

        data_line = line.split(':')
        vertex = data_line[0]
        neighbours = [data.strip()[:-1] for data in data_line[1].split()]

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

    def bron_kerbosch(self, P, R = [], X = []):
        if P + X == []:
            self.result.append(str(sorted(R)))
            return R

        vertex_index = 0
        while vertex_index < len(P):
            vertex = P[vertex_index]
            neighbours = set(self.graph[vertex])
        
            new_P = sorted(list(set(P).intersection(neighbours)))
            new_R = sorted(list(set(R).union({vertex})))
            new_X = sorted(list(set(X).intersection(neighbours)))

            self.bron_kerbosch(new_P, new_R, new_X)

            P = sorted(list(set(P).difference(vertex)))
            X = sorted(list(set(X).union(vertex)))

            vertex_index += 1

if __name__ == '__main__':
    cliques = Cliques("cliques_copas.txt")
    cliques.run()

    for result in cliques.result:
        if len(result) > 3:
            print(result)
