import pandas as pd
import numpy as np
from src.config import settings as st


def upsample(df: pd.DataFrame, col: str = "fradulent"):

    rng = np.random.RandomState(st.seed)
    UP = st.UPSAMPLE_PROB
    frad_index = df[df[col] == True].index.values
    repeated = rng.choice(frad_index, int(len(frad_index) * UP))
    df_final = pd.concat([df, df.loc[repeated]]).reset_index(drop=True)
    return df_final
