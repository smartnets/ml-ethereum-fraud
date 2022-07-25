# %%
import numpy as np
import pandas as pd
from src.utils.paths import get_path
from src.config import settings as st

# %%

LABELS = {
    "Legit": False,
    "Dodgy": True
}

def get_ground_truth():
    rnd = np.random.RandomState(st.seed)

    path = get_path("data/ground_truth.csv")
    df = pd.read_csv(path)
    df = df[df["Label"] != "Label"]
    df = df[["Address", "Label"]].copy().reset_index(drop=True)
    df.columns = ["address", "fradulent"]
    df = df.dropna()
    df["fradulent"] = df["fradulent"].map(LABELS)

    index = df.index.values
    rnd.shuffle(index)

    TEST_SIZE = int(index.shape[0] * st.test_size)
    test_index = index[:TEST_SIZE]
    train_index = index[TEST_SIZE:]

    df_train = df.loc[train_index]
    df_test = df.loc[test_index]

    return df_train, df_test

# %%
