import json
import sys
from pathlib import Path

THRESHOLDS = {
    "accuracy": 0.0,   # should not decrease accuracy
    "auc": 0.0,
    "loss": None       # not compare loss
}

def is_regression(metric, diff, threshold):
    """
    diff < 0  → performance down
    threshold → allow decent value
    """
    if diff is None:
        return False
    return diff < -threshold


def main(diff_path):
    diff_file = Path(diff_path)

    if not diff_file.exists():
        print("❗ metrics diff file not found – skipping regression check")
        sys.exit(0)

    with open(diff_file) as f:
        diff_data = json.load(f)

    # diff_data structure:
    # {
    #   "metrics/metrics.json": {
    #       "accuracy": {"old": 0.82, "new": 0.85, "diff": 0.03}
    #   }
    # }

    regressions = []

    for file, metrics in diff_data.items():
        for name, values in metrics.items():
            if name not in THRESHOLDS:
                continue

            threshold = THRESHOLDS[name]
            if threshold is None:
                continue

            diff = values.get("diff")

            if is_regression(name, diff, threshold):
                regressions.append(
                    f"{name}: {values.get('old')} → {values.get('new')} (diff={diff})"
                )

    if regressions:
        print("❌ Metric regression detected:")
        for r in regressions:
            print(f" - {r}")
        sys.exit(1)

    print("✅ No metric regression detected")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_regression.py <metrics_diff.json>")
        sys.exit(1)

    main(sys.argv[1])
