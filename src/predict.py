import joblib
import pandas as pd
import numpy as np
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Model paths
MODEL_PATH = PROJECT_ROOT / "models" / "rf_capped_fd001.pkl"
FEATURES_PATH = PROJECT_ROOT / "models" / "feature_columns_fd001.pkl"


# Load model and feature columns
model = joblib.load(MODEL_PATH)
feature_columns = joblib.load(FEATURES_PATH)


def predict_rul(input_data):
    """
    Predict Remaining Useful Life (RUL).

    Parameters
    ----------
    input_data : dict or pandas.DataFrame
        Sensor and operational-setting values.

    Returns
    -------
    numpy.ndarray
        Predicted RUL values in cycles.
    """

    # Convert dictionary to DataFrame
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Select features in exact training order
    X = input_data[feature_columns].copy()

    # Make prediction
    predictions = model.predict(X)

    # Keep predictions inside valid capped range
    predictions = np.clip(predictions, 0, 125)

    return predictions


if __name__ == "__main__":
    print("RUL prediction module loaded successfully!")
    print("Number of model features:", len(feature_columns))