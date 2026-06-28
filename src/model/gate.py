import json
import yaml
import sys
from pathlib import Path

METRICS_PATH = "metrics/metrics.json"
VALIDATION_PATH = "configs/model/validation.yaml"

# load files
metrics = json.load(open(METRICS_PATH))
validation = yaml.safe_load(open(VALIDATION_PATH))

gate = validation["gate"]

updated = False

# accuracy gate
if metrics["val_accuracy"] > gate["min_val_accuracy"]:
    gate["min_val_accuracy"] = round(metrics["val_accuracy"], 6)
    updated = True
elif metrics["val_accuracy"] < gate["min_val_accuracy"]:
    sys.exit("❌ Validation accuracy gate failed")

# f1 gate
if metrics["val_f1"] > gate["min_val_f1"]:
    gate["min_val_f1"] = round(metrics["val_f1"], 6)
    updated = True
elif metrics["val_f1"] < gate["min_val_f1"]:
    sys.exit("❌ Validation F1 gate failed")

# save updated gate if improved
if updated:
    Path(VALIDATION_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(VALIDATION_PATH, "w") as f:
        yaml.safe_dump(validation, f)
    print("⬆️ Validation gate updated with best metrics")

print("✅ Validation gate passed")
