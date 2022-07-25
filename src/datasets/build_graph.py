# %%
import networkx as nx
from src.utils.paths import get_path
from src.datasets.variations.index import DATASETS


MODES = {
    "simple": nx.Graph,
    "directed": nx.DiGraph,
    "multi": nx.MultiGraph,
    "mutli-di": nx.MultiDiGraph,
}


class BaseGraph:
    def __init__(self, mode: str = "simple"):

        self.base_class = MODES[mode]
        self.G = self.base_class()

    def load_from_file(self, prefix: str):

        edge_path = get_path(f"data/{prefix}_edges.csv")
        node_path = get_path(f"data/{prefix}_nodes.csv")

        node_parser, edge_parser = DATASETS[prefix]

        with open(edge_path, "r") as fh:
            for i, line in enumerate(fh):
                if i == 0:
                    continue

                from_, to_, features = edge_parser(line)
                self.G.add_edge(from_, to_, **features)

        with open(node_path, "r") as fh:
            features = {}
            for i, line in enumerate(fh):
                if i == 0:
                    continue
                addr, f = node_parser(line)
                features[addr] = f
            nx.set_node_attributes(self.G, features)


# %%

# %%
