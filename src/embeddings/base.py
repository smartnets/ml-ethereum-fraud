from src.datasets.build_graph import BaseGraph
from functools import cached_property


class Embedding:
    def __init__(self, graph: BaseGraph):

        self.graph = graph

    @cached_property
    def embedding(self):
        return self._compute_embedding()

    def _compute_embedding(self):
        pass