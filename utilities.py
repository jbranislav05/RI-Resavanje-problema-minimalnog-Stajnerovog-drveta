import copy
import sys
from graphviz import Graph as GraphV
import graphviz as gv
import random


class Utilities:

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
            node = not_visited.pop(0)
            visited.add(node)
            for neighbor in self.adjacency_list[node]:
                if((neighbor[0] not in visited and neighbor[0] not in not_visited) and neighbor[0] in node_list):
                    not_visited.append(neighbor[0])
                    node_list.remove(neighbor[0])
        if(node_list):
            return False
        return True

    def get_full_edge_information(self,edge_list):
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
