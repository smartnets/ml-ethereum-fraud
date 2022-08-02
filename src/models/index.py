from src.models.log_reg import get_logreg
from src.models.mlp import get_mlp
from src.models.xgb import get_xgb

MODELS = {
    "mlp": get_mlp,
    "xgb": get_xgb,
    "logreg": get_logreg,
}
