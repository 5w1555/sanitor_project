# sanitor/config.py
import json
from pathlib import Path
from typing import Dict, Any

DEFAULTS: Dict[str, Any] = {
    "magic_numbers":   {"ignore": [0,1,2,3,4,5], "min_repeats": 3},
    "duplicate_structure": {"min_statements": 3},
    "vague_naming":    {"threshold": 4},
}

def load_config(path: Path = None, overrides: Dict[str,Any] = None) -> Dict[str, Any]:
    cfg = DEFAULTS.copy()
    if path and path.exists():
        user = json.loads(path.read_text(encoding="utf-8"))
        for k,v in user.items():
            cfg[k] = {**cfg.get(k,{}), **v}
    if overrides:
        for k,v in overrides.items():
            cfg[k] = {**cfg.get(k,{}), **v} if isinstance(v, dict) else v
    return cfg
