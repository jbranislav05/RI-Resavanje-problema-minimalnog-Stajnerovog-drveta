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
        edges = set()
        for i in range(0, (len(nodes_list) - 1)):
            for edge in self.edge_list:
                if((edge[1] == nodes_list[i] and edge[2] == nodes_list[i+1]) or (edge[2] == nodes_list[i] and edge[1] == nodes_list[i+1])):
                    edges.add(edge[0])
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
        #print("Chosen node is " + str(random_terminal))
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
        for edge in E:
            self.solution.append(edge)
        for edge in self.edge_list:
            if edge[0] in E:
                total_weight = total_weight + int(edge[3])

        return E, total_weight

    def printSteiner(self, steiner_edges):
        g = GraphV('Gsa', filename='simulatedannealing.gv')  # , engine='sfdp')

        for edge in self.edge_list:
            if edge[0] in steiner_edges:
                color = "red"
            else:
                color = "green"
            g.edge(str(edge[1]), str(edge[2]), color=color)
        print(g.source)
        g.view()

    def simulatedAnnealing(self, maxIters, FirstSolution, terminal_vertices):

        currValue = FirstSolution

        bestValue = currValue
        i = 1
        k = 1
        while i < maxIters:
            terms = copy.deepcopy(terminal_vertices)
            old_solution = currValue
            newValue = self.random_solution(terms)
            # print(currValue[0],currValue[1]) #ispis trenutnog resenja
            if newValue[1] < currValue[1]:  # ako smo dobili manju tezinu
                currValue = newValue
            else:
                p = 1.0 / i ** 0.5
                q = random.uniform(0, 1)
                if p > q:
                    currValue = newValue
                else:
                    currValue = old_solution
            if newValue[1] < bestValue[1]:
                bestValue = newValue
            i += 1

        return bestValue

    def runSA(self, terminal_vertices):
        print(terminal_vertices)
        print("●▬▬▬▬ Pocetno resenje: ▬▬▬▬●")
        FirstSolution = self.random_solution(terminal_vertices)
        print(FirstSolution[0], FirstSolution[1])
        print()

        # -------------------------------------------------------------------------------------------------
        maxIters = 200000
        BestValue = self.simulatedAnnealing(
            maxIters, FirstSolution, terminal_vertices)
        print("●▬▬▬▬ Resenje simuliranim kaljenjem ▬▬▬▬●")
        print(BestValue[0], BestValue[1])
        self.printSteiner(BestValue[0])
