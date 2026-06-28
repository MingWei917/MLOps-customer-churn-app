import pandas as pd
import yaml

preprocess_yaml_path = "configs/data/preprocess.yaml"
cfg = yaml.safe_load(open(preprocess_yaml_path))

df = pd.read_csv(cfg["input"]["path"])

# drop columns
df = df.drop(columns=cfg["rules"]["drop_columns"])

# fill missing values
for col, value in cfg["rules"]["fill_na"].items():
    df[col] = df[col].fillna(value)

df.to_parquet(cfg["output"]["path"], index=False)

print("Preprocessing completed")
