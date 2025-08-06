# sanitor/checks/vague_naming.py
from sanitor.checks.registry import register
from sanitor.astdata import ASTData
from collections import Counter
from typing import List, Tuple

@register(name="vague_naming", severity="low")
def check_vague_naming(data: ASTData, cfg: dict) -> List[Tuple[int,str]]:
    threshold = cfg.get("threshold", 4)
    words = ['handle','process','do','get','set','run','manage']
    counts = Counter()
    for fn in data.functions:
        for tok in fn.name.lower().split('_'):
            if tok in words:
                counts[tok] += 1
    issues = []
    for w,ct in counts.items():
        if ct >= threshold:
            issues.append((1,
                f"Overused word '{w}' in {ct} functions – be more specific"))
    return issues
