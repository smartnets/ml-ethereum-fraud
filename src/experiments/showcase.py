# %%
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, accuracy_score

from src.config import settings as st
from src.datasets.ground_truth import get_ground_truth
from src.datasets.build_graph import BaseGraph
from src.embeddings.node2vec_plain import Node2VecPlain

# %%
DATASET = "both_ends_belong"

# %%
g = BaseGraph()
g.load_from_file(DATASET)

# %%

emb = Node2VecPlain(g)

# %%
embedding = emb.embedding
# %%

df_train, df_test = get_ground_truth()

# %%

# Filter missing nodes
nodes = g.G.nodes()
df_train = df_train[df_train["address"].isin(nodes)]
df_test = df_test[df_test["address"].isin(nodes)]

# %%

X_train = pd.DataFrame([embedding[x] for x in df_train["address"]])
X_train.index = df_train.index
y_train = df_train["fradulent"]

X_test = pd.DataFrame([embedding[x] for x in df_test["address"]])
X_test.index = df_test.index
y_test = df_test["fradulent"]

print(f"There are {y_test.sum()} positve examples out of {y_test.shape[0]}")
# %%

clf = MLPClassifier(random_state=st.seed, max_iter=st.model.epochs)
clf.fit(X_train, y_train)

# %%
y_pred = clf.predict(X_test)


# %%
f1 = f1_score(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)
print(f"Obtained F1-score: {f1:.2f}")
print(f"Obtained Accuracy: {acc:.2f}")

# %%