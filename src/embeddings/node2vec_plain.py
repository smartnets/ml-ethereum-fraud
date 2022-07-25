from src.embeddings.base import Embedding
from node2vec import Node2Vec
from src.config import settings as st


class Node2VecPlain(Embedding):
    def _compute_embedding(self):

        dim = st.embedding.dimension
        wl = st.embedding.walk_length
        nw = st.embedding.num_walks
        workers = st.embedding.workers
        window = st.embedding.window
        min_cnt = st.embedding.min_count

        node2vec = Node2Vec(
            self.graph.G,
            dimensions=dim,
            walk_length=wl,
            num_walks=nw,
            workers=workers,
            seed=st.seed,
        )
        model = node2vec.fit(
            window=window, min_count=min_cnt, batch_words=st.batch_size, seed=st.seed
        )

        self.model = model

        embeddings = {}
        for node in self.graph.G.nodes():
            embeddings[node] = model.wv[node]

        return embeddings
