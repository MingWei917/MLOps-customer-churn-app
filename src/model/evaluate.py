import json
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import joblib

# paths
MODEL_PATH = "models/model.pkl"
TEST_X = "data/split/test_features.parquet"
TEST_Y = "data/split/test_labels.parquet"
METRICS_PATH = "metrics/test_metrics.json"

def main():
    # load model
    model = joblib.load(MODEL_PATH)

    # load test data
    X_test = pd.read_parquet(TEST_X)
    y_test = pd.read_parquet(TEST_Y).iloc[:, 0]

    # predict
    y_pred = model.predict(X_test)

    # metrics
    metrics = {
        "test_accuracy": accuracy_score(y_test, y_pred),
        "test_f1": f1_score(y_test, y_pred),
    }

    # optional: AUC (if model supports predict_proba)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
        metrics["test_auc"] = roc_auc_score(y_test, y_proba)

    # save
    Path("metrics").mkdir(exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print("✅ Test evaluation completed")
    print(metrics)

if __name__ == "__main__":
    main()
