from sanitor.checks.registry import register
from sanitor.astdata import ASTData
from collections import defaultdict
from typing import List, Tuple

@register(name="duplicate_structure", severity="high")
def check_duplicate_structure(data: ASTData, cfg: dict) -> List[Tuple[int,str]]:
    """
    Detects functions with identical statement structure and argument count.
    Flags groups of functions that share the same sequence of statement types and number of arguments.
    """
    min_stmts = cfg.get("min_statements", 3)
    sig_map = defaultdict(list)
    for fn in data.functions:
        # Get the sequence of statement types in the function body
        stmts = [type(s).__name__ for s in fn.body]
        if len(stmts) < min_stmts:
            continue  # Skip short functions
        # Signature: (number of arguments, statement type sequence)
        sig = (len(fn.args.args), tuple(stmts))
        sig_map[sig].append(fn)
    issues = []
    for funcs in sig_map.values():
        if len(funcs) > 1:
            # Report all functions sharing the same structure
            names = [f.name for f in funcs]
            line = funcs[0].lineno
            issues.append((line,
                f"Functions with identical structure: {', '.join(names)}"))
    return issues
