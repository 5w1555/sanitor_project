# sanitor/checks/similar_names.py

import ast
from difflib import SequenceMatcher
from sanitor.engine import ASTData
from typing import List, Tuple

def check_similar_functions(data: ASTData, cfg: dict) -> List[Tuple[int, str]]:
    """
    Cluster function names that are too similar (possible copy-paste logic)
    and report one issue per cluster.
    """
    threshold = cfg.get("threshold", 0.8)
    min_body   = cfg.get("min_body", 1)  # only consider functions with > min_body statements
    
    # Build list of (name, lineno) for eligible functions
    funcs = [
        (fn.name, fn.lineno) 
        for fn in data.functions 
        if len(fn.body) > min_body and not fn.name.startswith('_')
    ]
    
    # Build adjacency: name -> set of similar names
    adj = {name: set() for name, _ in funcs}
    for i, (f1, _) in enumerate(funcs):
        for f2, _ in funcs[i+1:]:
            score = SequenceMatcher(None, f1.lower(), f2.lower()).ratio()
            if score > threshold:
                adj[f1].add(f2)
                adj[f2].add(f1)
    
    # DFS to extract connected components
    visited = set()
    issues = []
    for name, lineno in funcs:
        if name in visited or not adj[name]:
            continue
        
        # start a new component
        stack = [name]
        component = []
        while stack:
            curr = stack.pop()
            if curr in visited:
                continue
            visited.add(curr)
            component.append(curr)
            # add neighbors not yet visited
            for nbr in adj[curr]:
                if nbr not in visited:
                    stack.append(nbr)
        
        # report one issue per cluster
        # use the smallest lineno among the group
        first_line = min(ln for nm, ln in funcs if nm in component)
        issues.append((
            first_line,
            f"Similar function cluster: {', '.join(sorted(component))} (threshold {threshold})"
        ))
    
    return issues
