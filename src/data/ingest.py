import requests
from pathlib import Path
import yaml

ingest_cfg_path = "configs/data/ingest.yaml"
cfg = yaml.safe_load(open(ingest_cfg_path))

url = cfg["source"]["url"]
output_path = Path(cfg["output"]["path"])
output_path.parent.mkdir(parents=True, exist_ok=True)

response = requests.get(url)
output_path.write_bytes(response.content)

print(f"Downloaded data to {output_path}")
