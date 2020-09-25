import sys
from graphviz import Graph as GraphV
import graphviz as gv


class Steinerbf:
    def __init__(self, edge_list):
        self.adjacency_list = self.initialize(edge_list)
        self.edge_list = edge_list

    def __str__(self):
        return str(self.adjacency_list)

    def initialize(self, g_list):
        adjacency_list = {}
        for edge in g_list:
            adjacent_edges = (edge[2], edge[3])
            if(edge[1] in adjacency_list):
                tmp_value = adjacency_list.get(edge[1])
                tmp_value.append(adjacent_edges)
                adjacency_list.update({edge[1]: tmp_value})
            else:
                adjacency_list.update({edge[1]: [adjacent_edges]})
        for edge in g_list:
            adjacent_edges = (edge[1], edge[3])
            if(edge[2] in adjacency_list):
                tmp_value = adjacency_list.get(edge[2])
                tmp_value.append(adjacent_edges)
                adjacency_list.update({edge[2]: tmp_value})
            else:
                adjacency_list.update({edge[2]: [adjacent_edges]})
        return adjacency_list

    # Pronalazenje suseda cvora v
    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def dijkstra(self, start, stop):

        # Q je skup ovorenih cvorova, inicijalno sadrzi sve cvorove grafa
        Q = set([v for v in self.adjacency_list])

        # D sadrzi tekuce udaljenosti od polaznog cvora (start) do ostalih cvorova, inicijalno beskonacne
        D = dict([(v, float('inf')) for v in self.adjacency_list])

        # Udaljenost polaznog cvora od samog sebe je 0
        D[start] = 0

        # Mapa parents cuva roditelje cvorova
        parent = {}
        parent[start] = None

        iteration = 0

        # Dok je skup Q neprazan:
        while len(Q) > 0:

            # Pronalazi se cvor sa najmanjoj udaljenoscu od polaznog cvora i uklanja iz Q
            n = None
            iteration += 1

            for w in Q:
                if n == None or (D[w] != float('inf') and D[w] < D[n]):
                    n = w

            # Ako ne postoji cvor cija je udaljenost manja od beskonacnosti, put od polaznog do ciljnog cvora ne postoji
            if D[n] == float('inf'):
                print('Trazeni put ne postoji')
                print('Broj iteracija: ', iteration)
                return None

            if n == stop:
                path = []
                d_n = D[n]
                # do-while petlja ne postoji u Python-u
                while n != None:
                    path.append(n)
                    n = parent[n]

                path.reverse()

                #print('Pronadjen je put: {}'.format(path))
                #print('Broj iteracija: ', iteration)
                #print('Duzina puta je ', d_n)
                return path, d_n

            # proveri da li je ustanovljeno rastojanje od polaznog cvora do m vece od rastojanja
            # od polaznog cvora do m preko cvora n i ako jeste, promeniti informaciju
            # o roditelju cvora m na cvor n i upamtiti novo rastojanje.
            for (m, weight) in self.adjacency_list[n]:
                if D[m] == float('inf') or D[n] + weight < D[m]:
                    D[m] = D[n] + weight
                    parent[m] = n

            Q.remove(n)

        #  Obavesti da trazeni put ne postoji (Q je prazan skup i uspeh nije prijavljen).
        print('Trazeni put ne postoji')
        return None

    def get_edges_between_nodes(self, nodes_list):
        # [1,2,3,4,5]
        edges = set()
        for i in range(0, (len(nodes_list) - 1)):
            for edge in self.edge_list:
                if((edge[1] == nodes_list[i] and edge[2] == nodes_list[i+1]) or (edge[2] == nodes_list[i] and edge[1] == nodes_list[i+1])):
                    edges.add(edge[0])
        return edges

    def steiner(self, terminals):
        T = set()  # 1
        E = set()
        T.add(terminals.pop(0))  # 3 5 6
        total_sum = 0
        while(terminals):
            min_v = None
            path_to_V = None
            min_weight = sys.maxsize
            for v in terminals:
                for t in T:
                    (path, weight) = self.dijkstra(v, t)
                    if (weight <= min_weight):
                        min_weight = weight
                        path_to_V = path
                        min_v = v
            # print()
            #print("Current T is : " + str(T))
            #print("Chosen node is: " + str(min_v))
            #print("Path is :" + str(path))
            edges_used = self.get_edges_between_nodes(path)
            E = E | edges_used
            for node in path_to_V:
                T.add(node)
            terminals.remove(v)
            #print("Terminals left are : " + str(terminals))

        # print(T)
        for edge in self.edge_list:
            for e in E:
                if(str(e) == str(edge[0])):
                    total_sum = total_sum + int(edge[3])
        print("Total weight is : " + str(total_sum))
        print("Edges used are: " + str(E))
        # print(terminals)
        self.printSteiner(E)
        return E

    def printSteiner(self, steiner_edges):
        g = GraphV('G', filename='bruteforce.gv')  # , engine='sfdp')

        for edge in self.edge_list:
            if edge[0] in steiner_edges:
                color = "red"
            else:
                color = "green"
            g.edge(str(edge[1]), str(edge[2]),
                   color=color, weight=str(edge[3]))
        print(g.source)
        g.view()

    def runBF(self, terminals):
        print(self.steiner(terminals))

    # bfs - returns true if two nodes are connected
    def check_if_two_nodes_are_connected(self, start, end):
        visited = set()
        not_visited = []
        not_visited.append(start)
        while(not_visited):
            node = not_visited.pop(0)
            visited.add(node)
            for neighbor in self.adjacency_list[node]:
                if(neighbor[0] == end):
                    return True
                else:
                    if(neighbor[0] not in visited and neighbor[0] not in not_visited):
                        not_visited.append(neighbor[0])
        return False

    # bfs - returns true if nodes from the list form a connected graph
    def check_if_nodes_are_connected(self, node_list):  # indirectly
        visited = set()
        not_visited = []
        not_visited.append(node_list.pop(0))
        while(not_visited):
            node = not_visited.pop(0)
            visited.add(node)
            for neighbor in self.adjacency_list[node]:
                if((neighbor[0] not in visited and neighbor[0] not in not_visited) and neighbor[0] in node_list):
                    not_visited.append(neighbor[0])
                    node_list.remove(neighbor[0])
        if(node_list):
            return False
        return True

    def get_full_edge_information(self, edge_list):
        new_edge_list = []
        for edge in edge_list:
            for edgeFull in self.edge_list:
                if edge == edgeFull[0]:
                    new_edge_list.append[edgeFull]
        return new_edge_list

    def check_if_edges_are_connected(self, edge_list):
        new_edge_list = self.get_full_edge_information(edge_list)
        graph = self.initialize(new_edge_list)
        keys_list = list(graph.keys())
        return self.check_if_nodes_are_connected(keys_list)
