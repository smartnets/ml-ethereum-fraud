from src.config import settings as st
from sklearn.linear_model import LogisticRegression


def get_logreg():

    c = st.MODELS.LOGREG
    model = LogisticRegression(random_state=st.seed, C=c.C)
    return model
