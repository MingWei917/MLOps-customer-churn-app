import pandas as pd
import yaml
from pathlib import Path

feature_yaml_path = "configs/data/feature.yaml"

cfg = yaml.safe_load(open(feature_yaml_path))

# load
df = pd.read_parquet(cfg["input"]["path"])

num_cols = cfg["features"]["numeric"]
cat_cols = cfg["features"]["categorical"]
label_col = cfg["label"]["name"]

# numeric
X_num = df[num_cols]

# categorical → one-hot
X_cat = pd.get_dummies(
    df[cat_cols],
    prefix=cat_cols,
    drop_first=cfg["onehot_config"]["drop_first"]
)

# True / False → 1 / 0
X_cat = X_cat.astype(cfg["onehot_config"]["dtype"])

# combine
X = pd.concat([X_num, X_cat], axis=1)
#y = df[[label_col]]  # DataFrame keep
y = (
    df[[cfg["label"]["name"]]]
      .replace({
          cfg["label"]["positive"]: 1,
          cfg["label"]["negative"]: 0
      })
      .astype(cfg["label"]["dtype"])
)

# save features & labels
Path(cfg["output"]["features"]).parent.mkdir(parents=True, exist_ok=True)
X.to_parquet(cfg["output"]["features"], index=False)
y.to_parquet(cfg["output"]["labels"], index=False)

# save schema (importance)
schema = {
    "numeric_features": num_cols,
    "categorical_features": cat_cols,
    "encoded_features": list(X.columns)
}

with open(cfg["output"]["schema"], "w") as f:
    yaml.safe_dump(schema, f)

print("Feature generation with categorical encoding completed")
