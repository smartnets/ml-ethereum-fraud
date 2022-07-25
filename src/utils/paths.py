from src.config import settings as st
from pathlib import Path


def get_path(path: str):
    return Path(st.ROOT_DIR) / path