import yaml
import os
from pathlib import Path

def load_config():
    # Finds the path regardless of where the script is run
    base_path = Path(__file__).resolve().parent.parent
    config_path = base_path / "config" / "config.yaml"
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()