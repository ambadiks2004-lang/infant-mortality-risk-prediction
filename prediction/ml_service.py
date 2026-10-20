from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from django.conf import settings

MODEL_PATH = settings.BASE_DIR / "ml_models" / "xgboost_infant_mortality.pkl"
PREPROCESS_PATH = settings.BASE_DIR / "ml_models" / "xgb_preprocessing.pkl"
THRESHOLD = 0.50

class ModelArtifactError(Exception):
    pass

def _load_artifacts():
    if not MODEL_PATH.exists() or not PREPROCESS_PATH.exists():
        missing = []
        if not MODEL_PATH.exists():
            missing.append(str(MODEL_PATH))
        if not PREPROCESS_PATH.exists():
            missing.append(str(PREPROCESS_PATH))
        raise ModelArtifactError(
            "Trained model files are missing. Copy these files into ml_models/: " + ", ".join(missing)
        )
    try:
        model = joblib.load(MODEL_PATH)
        prep = joblib.load(PREPROCESS_PATH)
    except Exception as exc:
        raise ModelArtifactError(
            "Could not load the saved model/preprocessing files. Check that their package versions match training."
        ) from exc
    return model, prep

def _encode_sex(value, prep):
    mapping = prep.get("sex_mapping", {"M": 1, "F": 0})
    if value in mapping:
        return mapping[value]
    # Some saved pipelines use the opposite mapping; defer to the saved mapping.
    return np.nan

def predict_infant(mother, infant):
    model, prep = _load_artifacts()
    raw = {
        "mother_age": mother.mother_age,
        "education": mother.education,
        "prenatal_visits": mother.prenatal_visits,
        "cigarettes": mother.cigarettes,
        "bmi": mother.bmi,
        "pre_diabetes": int(mother.pre_diabetes),
        "gest_diabetes": int(mother.gest_diabetes),
        "pre_hypertension": int(mother.pre_hypertension),
        "gest_hypertension": int(mother.gest_hypertension),
        "apgar5": infant.apgar5,
        "plurality": infant.plurality,
        "infant_sex": _encode_sex(infant.infant_sex, prep),
        "gestational_age": infant.gestational_age,
        "birth_weight": infant.birth_weight,
    }

    feature_columns = prep.get("feature_columns")
    if not feature_columns:
        raise ModelArtifactError("The preprocessing file has no 'feature_columns' list.")

    X = pd.DataFrame([raw])
    # Add any expected columns absent from this app's raw mapping as missing values.
    for col in feature_columns:
        if col not in X.columns:
            X[col] = np.nan
    X = X[feature_columns].copy()

    for col, code in prep.get("unknown_codes", {}).items():
        if col in X.columns:
            X.loc[X[col] == code, col] = np.nan

    X = X.replace({None: np.nan})
    X = X.fillna(prep.get("median_values", {})).astype(float)

    try:
        probability = float(model.predict_proba(X)[:, 1][0])
        predicted = int(probability >= THRESHOLD)
    except Exception as exc:
        raise ModelArtifactError(
            "Prediction failed. Verify that the model and preprocessing artifacts match the 14-feature training pipeline."
        ) from exc

    return predicted, probability, raw
