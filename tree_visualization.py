from __future__ import annotations
from typing import Any
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import igraph as ig
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go
from tree import HuffmanTree, Node


nr_vertices = 14
v_label = list(map(str, range(nr_vertices)))
G = Graph.Tree(nr_vertices, 2) # 2 stands for children number
lay = G.layout('rt')

position = {k: lay[k] for k in range(nr_vertices)}
Y = [lay[k][1] for k in range(nr_vertices)]
M = max(Y)

es = EdgeSeq(G) # sequence of edges
E = [e.tuple for e in G.es] # list of edges

L = len(position)
Xn = [position[k][0] for k in range(L)]
Yn = [2*M-position[k][1] for k in range(L)]
Xe = []
Ye = []
for edge in E:
    Xe+=[position[edge[0]][0],position[edge[1]][0], None]
    Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

labels = v_label

fig = go.Figure()
fig.add_trace(go.Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line=dict(color='rgb(210,210,210)', width=1),
                   hoverinfo='none'
                   ))
fig.add_trace(go.Scatter(x=Xn,
                  y=Yn,
                  mode='markers',
                  name='bla',
                  marker=dict(symbol='circle-dot',
                                size=18,
                                color='#6175c1',    #'#DB4551',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                  text=labels,
                  hoverinfo='text',
                  opacity=0.8
                  ))

axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            )

fig.write_image('graph.png')

def tree_visualization(tree: HuffmanTree) -> None:
    """
    This is the function that allows us to visualize a tree given the dict of
    the frequency of the characters
    """
    # display_tree = Graph.Tree()
    # lay = tree.layot('rt')

    # Given the huffman tree, keep track of the verticies and the edges
    # and use that to create the graph
    verticies = []
    edges = []
    get_edges_and_verticies(tree, verticies, edges)

    graph = Graph.DictList(verticies, edges)

    layout = graph.layout_reingold_tilford

    ig.plot(graph, layout)



def get_edges_and_verticies(tree: HuffmanTree, final_verticies = [], final_edges = []) -> None:
    """
    Recursively mutate final_verticies and final_edges 
    """

    if tree._root is None:
        pass

    else:
        instant_vertices_dict = {}
        instant_vertices_dict['frequency'] = tree._root.frequency
        if tree._root.character is not None:
            instant_vertices_dict['character'] = tree._root.character
        else:
            instant_vertices_dict['character'] = ''

        final_verticies.append(instant_vertices_dict)
        
        instant_edges_dict = {}
        if tree._right is not None:
            instant_edges_dict['source'] = tree._root.frequency
            instant_edges_dict['target'] = tree._right._root.frequency
            instant_edges_dict['bit'] = 1
            final_edges.append(instant_edges_dict)
            get_edges_and_verticies(tree._right, final_verticies, final_edges)
        elif tree._left is not None:
            instant_edges_dict['source'] = tree._root.frequency
            instant_edges_dict['target'] = tree._left._root.frequency
            instant_edges_dict['bit'] = 0
            final_edges.append(instant_edges_dict)
            get_edges_and_verticies(tree._left, final_verticies, final_edges)


