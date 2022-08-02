from sklearn.neural_network import MLPClassifier
from src.config import settings as st


def get_mlp():

    c = st.MODELS.MLP

    model = MLPClassifier(
        hidden_layer_sizes=tuple(c.hidden_layer_sizes),
        random_state=st.seed,
        max_iter=c.max_iter,
    )
    return model
