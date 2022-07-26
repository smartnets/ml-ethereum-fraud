# %%
import dgl
import torch
import torch.nn as nn
import torch.nn.functional as F
import itertools
import numpy as np
import scipy.sparse as sp
import dgl.data
from dgl.nn import SAGEConv
import dgl.function as fn
from sklearn.metrics import roc_auc_score

from src.config import settings as st
from src.datasets.build_graph import BaseGraph
from src.embeddings.base import Embedding

class GraphSAGE(nn.Module):
    def __init__(self, in_feats, h_feats):
        super(GraphSAGE, self).__init__()
        self.conv1 = SAGEConv(in_feats, h_feats, 'mean')
        self.conv2 = SAGEConv(h_feats, h_feats, 'mean')

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        return h

class DotPredictor(nn.Module):
    def forward(self, g, h):
        with g.local_scope():
            g.ndata['h'] = h
            # Compute a new edge feature named 'score' by a dot-product between the
            # source node feature 'h' and destination node feature 'h'.
            g.apply_edges(fn.u_dot_v('h', 'h', 'score'))
            # u_dot_v returns a 1-element vector for each edge so you need to squeeze it.
            return g.edata['score'][:, 0]

def compute_loss(pos_score, neg_score):
    scores = torch.cat([pos_score, neg_score])
    labels = torch.cat([torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])])
    return F.binary_cross_entropy_with_logits(scores, labels)

def compute_auc(pos_score, neg_score):
    scores = torch.cat([pos_score, neg_score]).numpy()
    labels = torch.cat(
        [torch.ones(pos_score.shape[0]), torch.zeros(neg_score.shape[0])]).numpy()
    return roc_auc_score(labels, scores)

class GNNSageEmbedding(Embedding):
    def __init__(self, graph: BaseGraph):

        self.graph = graph
        self.g = dgl.from_networkx(graph.G)

        N = self.graph.G.number_of_nodes()
        self.feat = torch.Tensor(
            np.array(
                [[x[1]["isECR"], x[1]["isMiner"], i / N] for i, x in enumerate(graph.G.nodes(data=True))]
            ).reshape(N, -1)
        )


    def _compute_embedding(self):
        g = self.g
        u, v = g.edges()

        eids = np.arange(g.number_of_edges())
        eids = np.random.permutation(eids)
        test_size = int(len(eids) * 0.1)
        train_size = g.number_of_edges() - test_size
        test_pos_u, test_pos_v = u[eids[:test_size]], v[eids[:test_size]]
        train_pos_u, train_pos_v = u[eids[test_size:]], v[eids[test_size:]]

        # Find all negative edges and split them for training and testing
        adj = sp.coo_matrix((np.ones(len(u)), (u.numpy(), v.numpy())))
        adj_neg = 1 - adj.todense() - np.eye(g.number_of_nodes())
        neg_u, neg_v = np.where(adj_neg != 0)

        neg_eids = np.random.choice(len(neg_u), g.number_of_edges())
        test_neg_u, test_neg_v = neg_u[neg_eids[:test_size]], neg_v[neg_eids[:test_size]]
        train_neg_u, train_neg_v = neg_u[neg_eids[test_size:]], neg_v[neg_eids[test_size:]]

        train_g = dgl.remove_edges(g, eids[:test_size])

        train_pos_g = dgl.graph((train_pos_u, train_pos_v), num_nodes=g.number_of_nodes())
        train_neg_g = dgl.graph((train_neg_u, train_neg_v), num_nodes=g.number_of_nodes())

        test_pos_g = dgl.graph((test_pos_u, test_pos_v), num_nodes=g.number_of_nodes())
        test_neg_g = dgl.graph((test_neg_u, test_neg_v), num_nodes=g.number_of_nodes())



        model = GraphSAGE(self.feat.shape[1], 32)
        # You can replace DotPredictor with MLPPredictor.
        #pred = MLPPredictor(16)
        pred = DotPredictor()



# ----------- 3. set up loss and optimizer -------------- #
# in this case, loss will in training loop
        optimizer = torch.optim.Adam(itertools.chain(model.parameters(), pred.parameters()), lr=0.01)

# ----------- 4. training -------------------------------- #
        all_logits = []
        for e in range(1000):
            # forward
            h = model(train_g, self.feat)
            pos_score = pred(train_pos_g, h)
            neg_score = pred(train_neg_g, h)
            loss = compute_loss(pos_score, neg_score)

            # backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if e % 5 == 0:
                print('In epoch {}, loss: {}'.format(e, loss))

        # ----------- 5. check results ------------------------ #
        with torch.no_grad():
            pos_score = pred(test_pos_g, h)
            neg_score = pred(test_neg_g, h)
            print('AUC', compute_auc(pos_score, neg_score))

        return dict((
            x, h[i, :]) for i, x in enumerate(list(self.graph.G.nodes()))
        )


# Thumbnail credits: Link Prediction with Neo4j, Mark Needham
# sphinx_gallery_thumbnail_path = '_static/blitz_4_link_predict.png'
# %%
