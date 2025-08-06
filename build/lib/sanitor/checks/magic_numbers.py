# sanitor/checks/magic_numbers.py
from sanitor.checks.registry import register
from sanitor.astdata import ASTData
from collections import Counter
from typing import List, Tuple

@register(name="magic_numbers", severity="medium")
def check_magic_numbers(data: ASTData, cfg: dict) -> List[Tuple[int,str]]:
    ignore = set(cfg.get("ignore", []))
    min_rep = cfg.get("min_repeats", 3)
    # collect all literals > 2 that aren’t whitelisted
    vals = [n.value for n in data.constants
            if isinstance(n.value, (int, float)) and abs(n.value)>2 and n.value not in ignore]
    counts = Counter(vals)
    issues = []
    for val, freq in counts.items():
        if freq >= min_rep:
            # find one lineno for reporting
            line = next(n.lineno for n in data.constants if n.value == val)
            issues.append((line,
                f"Magic number {val} appears {freq}× – consider a named constant"))
    return issues
