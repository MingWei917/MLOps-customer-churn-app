import pandas as pd
import yaml
from sklearn.model_selection import train_test_split
from pathlib import Path

# paths
FEATURE_PATH = "data/features/feature.parquet"
LABEL_PATH = "data/features/label.parquet"
CONFIG_PATH = "configs/data/split.yaml"
OUT_DIR = Path("data/split")

OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)["split"]

def main():
    cfg = load_config()

    X = pd.read_parquet(FEATURE_PATH)
    y = pd.read_parquet(LABEL_PATH).iloc[:, 0]

    stratify = y if cfg["stratify"] else None

    # 1️ train+val / test split
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X,
        y,
        test_size=cfg["test_size"],
        random_state=cfg["random_state"],
        stratify=stratify,
    )

    # 2️ train / val split
    val_ratio = cfg["val_size"] / (1 - cfg["test_size"])
    stratify_tv = y_train_val if cfg["stratify"] else None

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=val_ratio,
        random_state=cfg["random_state"],
        stratify=stratify_tv,
    )

    # save
    X_train.to_parquet(OUT_DIR / "train_features.parquet")
    y_train.to_frame().to_parquet(OUT_DIR / "train_labels.parquet")

    X_val.to_parquet(OUT_DIR / "val_features.parquet")
    y_val.to_frame().to_parquet(OUT_DIR / "val_labels.parquet")

    X_test.to_parquet(OUT_DIR / "test_features.parquet")
    y_test.to_frame().to_parquet(OUT_DIR / "test_labels.parquet")

    print("✅ Data split completed")
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

if __name__ == "__main__":
    main()
