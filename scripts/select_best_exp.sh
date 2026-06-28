#!/bin/bash
set -e

BEST_EXP=$(dvc exp show \
  --sort-by metrics.val_accuracy \
  --sort-order desc \
  --no-pager | awk 'NR==3 {print $1}')

echo "Best experiment: $BEST_EXP"

dvc exp apply $BEST_EXP
