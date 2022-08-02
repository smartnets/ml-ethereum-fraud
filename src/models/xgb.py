from xgboost import XGBClassifier
from src.config import settings as st


def get_xgb():

    c = st.MODELS.XGB

    model = XGBClassifier(
        n_estimators=c.num_trees,
        max_depth=c.max_depth,
        learning_rate=c.learning_rate,
        random_state=st.seed,
    )
    return model
