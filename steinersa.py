import copy
import sys
from graphviz import Graph as GraphV
import graphviz as gv
import random


class Steinersa:
    def __init__(self, edge_list):
        self.adjacency_list = self.initialize(edge_list)
        self.edge_list = edge_list
        self.solution = []
        self.weight = 0
        self.old_solution = []
        self.old_weight = 0

    def __str__(self):
        return str(self.adjacency_list)

    def initialize(self, g_list):
        adjacency_list = {}
        for edge in g_list:
            adjacent_edges = (edge[2], edge[3], edge[0])
            if(edge[1] in adjacency_list):
                tmp_value = adjacency_list.get(edge[1])
                tmp_value.append(adjacent_edges)
                adjacency_list.update({edge[1]: tmp_value})
            else:
                adjacency_list.update({edge[1]: [adjacent_edges]})
        for edge in g_list:
            adjacent_edges = (edge[1], edge[3], edge[0])
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

    def get_edges_between_nodes(self, nodes_list):
        # [1,2,3,4,5]
        edges = []
        for i in range(0, (len(nodes_list) - 1)):
            for edge in self.edge_list:
                if((edge[1] == nodes_list[i] and edge[2] == nodes_list[i+1]) or (edge[2] == nodes_list[i] and edge[1] == nodes_list[i+1])):
                    edges.append(edge)
        return edges

    def dfs(self, adjacency_list, node, parentnode, parentedge, visited, parents, parentedges):

        if node not in visited:
            visited.append(node)
            parents[node] = parentnode
            parentedges[node] = parentedge
            for n in adjacency_list[node]:
                self.dfs(adjacency_list, n[0], node, n[2],
                         visited, parents, parentedges)
        return visited, parents, parentedges

    def random_solution(self, terminal_vertices):
        total_weight = 0
        T = set()
        E = set()
        terms = terminal_vertices
        # print(terms)
        random_terminal = random.sample(terms, 1)[0]  # npr { 3 }
        T.add(random_terminal)
        terms.remove(random_terminal)  # npr { 1 , 5 , 6 }
        shuffled_adjacency_list = copy.deepcopy(self.adjacency_list)
        for node, neighbors in shuffled_adjacency_list.items():
            random.shuffle(neighbors)
        visited, parents, parentedges = self.dfs(
            shuffled_adjacency_list, random_terminal, 0, None, [], {}, {})
        # print("Chosen node is " + str(random_terminal))
        # print("Parents-------")
        # print(parents)
        # print("parentedges-----")
        # print(parentedges)
        tmp_parent = None
        for term in terms:
            # print(term)
            tmp_parent = parents[term]
            parent_edge = parentedges[term]
            E.add(parent_edge)
            # sve dok se nismo vratili skroz od terma do neke tacke vec u T, dodaj roditelje i idi unazad
            while(tmp_parent not in T):
                # print("tmp_parent is " + str(tmp_parent) +
                #      " and parent_edge is " + str(parent_edge))
                T.add(tmp_parent)
                # bitno je da ovo bude prvo, da ne bismo preskocili granu
                parent_edge = parentedges[tmp_parent]
                E.add(parent_edge)
                tmp_parent = parents[tmp_parent]
            T.add(term)
        self.solution.clear()
        self.weight = 0
        for edge in E:
            for e in self.edge_list:
                if edge == e[0]:
                    self.solution.append(tuple(e))
        for edge in self.edge_list:
            if edge[0] in E:
                total_weight = total_weight + int(edge[3])
        self.weight = total_weight
        self.solution = self.sort_tuple_list(self.solution)
        return E, total_weight

    def sort_tuple_list(self, tup):
        tup.sort(key=lambda x: x[1])
        return tup

    def printSteiner(self, steiner_edges):
        g = GraphV('Gsa', filename='simulatedannealing.gv')  # , engine='sfdp')

        for edge in self.edge_list:
            if tuple(edge) in steiner_edges:
                color = "red"
            else:
                color = "green"
            g.edge(str(edge[1]), str(edge[2]), color=color)
        print(g.source)
        g.view()

    def anneal(self, terminal_vertices):
        a = random.randint(0, len(self.solution)-3)
        # we get 2 random numbers for selecting edges 2-3 from our solution graph
        b = a + random.randint(1, 2) + 1
        selected_edges = self.solution[a:b]
        for i in range(0, (len(selected_edges) - 1)):
            if(selected_edges[i][2] != selected_edges[i+1][1]):
                return False  # we check if the selected edges connect one to another
        for i in range(1, len(selected_edges)):
            if(selected_edges[i][1] in terminal_vertices):
                return False  # we check if connected edges contain any of the terminals between them
        self.old_solution = copy.deepcopy(self.solution)
        self.old_weight = self.weight
        for edge in selected_edges:
            # we remove the selected edges, so we can add new ones found by dijsktra
            self.solution.remove(edge)
            self.weight = self.weight - edge[3]
        # print(selected_edges)
        starting_node = selected_edges[0][1]
        ending_node = selected_edges[-1][2]
        # print(starting_node)
        # print(ending_node)
        (path, weight) = self.dijkstra(starting_node, ending_node)
        # print(path)
        edges_used = self.get_edges_between_nodes(path)
        for e in edges_used:
            self.solution.append(tuple(e))
            self.weight = self.weight + e[3]
        self.solution = self.sort_tuple_list(self.solution)
        return True

    def revert(self):
        self.solution = copy.deepcopy(self.old_solution)
        self.weight = self.old_weight

    def simulatedAnnealing(self, maxIters, FirstSolution, terminal_vertices):

        bestValue = FirstSolution
        i = 1
        while i < maxIters:
            terms = copy.deepcopy(terminal_vertices)
            # old_solution = currValue
            anneal_success = self.anneal(terms)
            if(anneal_success):
                if self.weight > self.old_weight:
                    p = 1.0 / i ** 0.5
                    q = random.uniform(0, 1)
                    if p > q:
                        pass
                        # we let the worse solution stay
                    else:
                        self.revert()
            if self.weight < bestValue[1]:
                bestValue = (self.solution, self.weight)
            i += 1
            if(i % 10000 == 0):
                self.old_solution = copy.deepcopy(self.solution)
                self.old_weight = self.weight
                self.random_solution(terms)
                if(self.old_weight < self.weight):
                    self.revert()

        return bestValue

    def runSA(self, terminal_vertices):
        print(terminal_vertices)
        print("●▬▬▬▬ Pocetno resenje: ▬▬▬▬●")
        terms = copy.deepcopy(terminal_vertices)
        FirstSolution = self.random_solution(terms)
        print(FirstSolution[0], FirstSolution[1])
        print()

        # -------------------------------------------------------------------------------------------------
        maxIters = 200000
        BestValue = self.simulatedAnnealing(
            maxIters, FirstSolution, terminal_vertices)
        print("●▬▬▬▬ Resenje simuliranim kaljenjem ▬▬▬▬●")
        print(BestValue[0], BestValue[1])
        self.printSteiner(BestValue[0])

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
    def check_if_nodes_are_connected(self, node_list):
        visited = set()
        not_visited = []
        not_visited.append(node_list.pop(0))
        while(not_visited):
            # print("Remaining nodes:")
            # print(node_list)
            node = not_visited.pop(0)
            # print(node)
            visited.add(node)
            # print("Not visited nodes")
            # print(not_visited)
            for neighbor in self.adjacency_list[node]:
                if((neighbor[0] not in visited and neighbor[0] not in not_visited) and neighbor[0] in node_list):
                    not_visited.append(neighbor[0])
                    node_list.remove(neighbor[0])
        # print(node_list)
        if(node_list):
            return False
        return True

    def get_full_edge_information(self, edge_list):
        new_edge_list = []
        for edge in edge_list:
            for edgeFull in self.edge_list:
                if edge == edgeFull[0]:
                    new_edge_list.append(tuple(edgeFull))
        return new_edge_list

    def check_if_edges_are_connected(self, edge_list):
        new_edge_list = self.get_full_edge_information(edge_list)
        graph = self.initialize(new_edge_list)
        keys_list = list(graph.keys())
        return (self.check_if_nodes_are_connected(keys_list))

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

                # print('Pronadjen je put: {}'.format(path))
                # print('Broj iteracija: ', iteration)
                # print('Duzina puta je ', d_n)
                return path, d_n

            # proveri da li je ustanovljeno rastojanje od polaznog cvora do m vece od rastojanja
            # od polaznog cvora do m preko cvora n i ako jeste, promeniti informaciju
            # o roditelju cvora m na cvor n i upamtiti novo rastojanje.
            for (m, weight, name) in self.adjacency_list[n]:
                if D[m] == float('inf') or D[n] + weight < D[m]:
                    D[m] = D[n] + weight
                    parent[m] = n

            Q.remove(n)

        #  Obavesti da trazeni put ne postoji (Q je prazan skup i uspeh nije prijavljen).
        print('Trazeni put ne postoji')
        return None
