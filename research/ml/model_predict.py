import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "kidney_model.pkl"
_model = None
_model_load_error = None


def _load_model():
    """Lazily load the model. If loading fails, keep the original
    exception and raise a clear RuntimeError on subsequent calls.
    """
    global _model, _model_load_error
    if _model is None and _model_load_error is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception as e:
            # Store the error so import-time doesn't crash the app; raise
            # a clear message when a prediction is actually requested.
            _model_load_error = e
    if _model_load_error is not None:
        msg = f"Failed to load model from {MODEL_PATH}: {type(_model_load_error).__name__}: {_model_load_error}"
        # Provide additional troubleshooting hint for sklearn version issues
        if isinstance(_model_load_error, AttributeError) or "InconsistentVersionWarning" in str(_model_load_error):
            msg += (
                "\nHint: The model was pickled with a different scikit-learn "
                "version. Either install the scikit-learn version used to "
                "train the model, or re-train / re-save the model with the "
                "current scikit-learn version."
            )
        raise RuntimeError(msg) from _model_load_error
    return _model


def predict_ckd(data: dict):
    model = _load_model()
    sample = pd.DataFrame([data])

    if hasattr(model, "feature_names_in_"):
        sample = sample.reindex(columns=model.feature_names_in_, fill_value=0)

    pred = model.predict(sample)[0]
    return int(pred)
