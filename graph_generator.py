from __future__ import annotations
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pathlib import Path
import random
import sys
import hashlib
import os

OUTPUT_DIR = "tester_files/generated"
MIN_NODE = 1
MAX_NODE = 50


@dataclass()
class Graph:
    graph: nx.Graph

    def to_exercise_format(self) -> str:
        n = len(self.graph.nodes)
        lines = [str(n)]
        for node in sorted(self.graph.nodes):
            neighs = ' '.join(str(key) for key in self.graph.neighbors(node))
            if len(neighs) == 0:
                lines.append('-')
            else:
                lines.append(neighs)
        return "\n".join(lines)+"\n"

    def draw(self, path: str):
        plt.title(f'Graph of {Path(path).stem}')
        pos = graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph, pos, with_labels=True, arrows=True)
        plt.savefig(path)
        plt.clf()



def gen_valid_trees(nodes: int, rand: random.Random):
    """ Generates a tree, saves it as an input file as well as image"""
    print(f"Generating a tree with {nodes} nodes")
    tree = nx.generators.random_tree(n=nodes, seed=rand)
    # 'tree' is undirected, use 'BFS' to get directed representation
    tree = nx.bfs_tree(tree, 0)
    tree = randomize_nodes(tree)
    graph = Graph(tree)

    # writing input file and image
    exercise_str = graph.to_exercise_format()
    # hash to avoid duplicate tests
    hasher = hashlib.md5()
    hasher.update(exercise_str.rstrip("\r\n").encode('utf-8'))
    ex_hash = hasher.hexdigest()
    name = f"valid-{nodes}-{ex_hash}"
    with open(Path(OUTPUT_DIR) / f"{name}.txt", 'w') as file:
        file.write(exercise_str)

    graph.draw(Path(OUTPUT_DIR) / f"{name}.png")


def randomize_nodes(graph: nx.Graph) -> nx.Graph:
    """ Randomizes keys in given graph, returning the updated graph """
    nodes = [i for i in range(len(graph.nodes))]
    random.shuffle(nodes)
    mapping = {orig:new for orig, new in zip(graph.nodes, nodes)}
    return nx.relabel_nodes(graph, mapping, True)


if __name__ == '__main__':
    seed = os.urandom(2500)
    random = random.Random(seed)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for node_count in range(1, MAX_NODE + 1):
        gen_valid_trees(node_count, random)
    print(f"Finished generating {MAX_NODE+1 - MIN_NODE} trees")