import json
import yaml
import pandas as pd
from pathlib import Path
import os
import joblib
import subprocess 

from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

import mlflow
import mlflow.sklearn

try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None

#MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:30500")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

CFG_PATH = "configs/model/train.yaml"

TRAIN_X = "data/split/train_features.parquet"
TRAIN_Y = "data/split/train_labels.parquet"
VAL_X = "data/split/val_features.parquet"
VAL_Y = "data/split/val_labels.parquet"


def load_config():
    with open(CFG_PATH, "r") as f:
        return yaml.safe_load(f)


def build_pipeline(model_name, params):
    if model_name == "logistic_regression":
        return Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(**params)),
            ]
        )

    if model_name == "random_forest":
        return Pipeline(
            steps=[
                ("model", RandomForestClassifier(**params)),
            ]
        )

    if model_name == "xgboost":
        if XGBClassifier is None:
            raise ImportError("xgboost is not installed")
        return Pipeline(
            steps=[
                ("model", XGBClassifier(**params)),
            ]
        )

    raise ValueError(f"Unknown model: {model_name}")

def get_git_commit_hash():
    """Get the current Git commit hash to link MLflow runs with DVC versions in MinIO."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"

def main():
    cfg = load_config()
    model_cfg = cfg["model"]

    model_name = model_cfg["name"]
    model_params = model_cfg["params"]

    mlflow.set_experiment("customer_churn-v1")

    with mlflow.start_run():
        mlflow.set_tags({
            "git_branch": os.getenv("GITHUB_REF_NAME", "local"),
            "git_sha": os.getenv("GITHUB_SHA", "local"),
            "dvc_commit": get_git_commit_hash(), # 🔗 Links MLflow metrics to DVC/MinIO artifacts
            "stage": "train",
        })

        mlflow.log_param("model", model_name)
        mlflow.log_params(model_params)

        X_train = pd.read_parquet(TRAIN_X)
        y_train = pd.read_parquet(TRAIN_Y).iloc[:, 0]
        X_val = pd.read_parquet(VAL_X)
        y_val = pd.read_parquet(VAL_Y).iloc[:, 0]

        pipeline = build_pipeline(model_name, model_params)

        pipeline.fit(X_train, y_train)

        val_preds = pipeline.predict(X_val)

        metrics = {
            "val_accuracy": accuracy_score(y_val, val_preds),
            "val_f1": f1_score(y_val, val_preds),
        }

        mlflow.log_metrics(metrics)

        # mlflow.sklearn.log_model(
        #     sk_model=pipeline,
        #     artifact_path="model",
        #     registered_model_name="customer_churn_model"
        # )

        Path("models").mkdir(exist_ok=True)
        Path("metrics").mkdir(exist_ok=True)

        joblib.dump(pipeline, "models/model.pkl")

        with open("metrics/metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        print("✅ Training completed")
        print(f"📊 Metrics: {metrics}")
        print(f"💾 Model saved to models/model.pkl (DVC will push to MinIO)")
        print(f"🔗 Metrics logged to MLflow at {MLFLOW_TRACKING_URI}")


if __name__ == "__main__":
    main()
