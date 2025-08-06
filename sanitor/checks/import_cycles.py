from collections import defaultdict
from pathlib import Path
from typing import List, Tuple, Set, Dict
import ast


def check_import_cycles(data, cfg) -> List[Tuple[int, str]]:
    """
    Detects import cycles between Python modules using Tarjan's algorithm.
    Returns a list of issues for each cycle found.
    """
    min_cycle_size = cfg.get("min_cycle_size", 2)
    
    # Build dependency graph: file -> set of imported files
    graph = defaultdict(set)
    for file_path, tree in data.file_trees.items():
        graph.setdefault(file_path, set())  # Ensure every file appears
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    resolved = _resolve_import_alias(alias.name, file_path.parent)
                    if resolved:
                        graph[file_path].add(resolved)
            elif isinstance(node, ast.ImportFrom) and node.module:
                resolved = _resolve_import_alias(node.module, file_path.parent)
                if resolved:
                    graph[file_path].add(resolved)
    
    # Convert to regular dict to prevent modification during iteration
    graph = dict(graph)
    
    # Tarjan's algorithm for finding strongly connected components (SCCs)
    index = {}
    lowlink = {}
    stack = []
    on_stack = set()
    current_index = 0
    components = []
    
    def tarjan_dfs(node: Path):
        nonlocal current_index
        # Assign index and lowlink
        index[node] = current_index
        lowlink[node] = current_index
        current_index += 1
        stack.append(node)
        on_stack.add(node)
        # Visit dependencies
        for dependency in graph.get(node, set()):
            if dependency not in index:
                tarjan_dfs(dependency)
                lowlink[node] = min(lowlink[node], lowlink[dependency])
            elif dependency in on_stack:
                lowlink[node] = min(lowlink[node], index[dependency])
        # If node is root of SCC, pop stack
        if lowlink[node] == index[node]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == node:
                    break
            if len(component) >= min_cycle_size:
                components.append(component)
    
    # Process all nodes (snapshot keys to avoid dict modification issues)
    nodes_to_process = list(graph.keys())
    for node in nodes_to_process:
        if node not in index:
            tarjan_dfs(node)
    
    # Convert components to issue reports
    issues = []
    for component in components:
        try:
            # Use relative paths for cleaner output
            paths = [str(p.relative_to(Path.cwd())) for p in component]
        except ValueError:
            # Fallback if relative_to fails
            paths = [str(p) for p in component]
        
        line = 1  # Could be enhanced to find actual import line
        message = f"Import cycle detected among modules: {' -> '.join(paths)}"
        issues.append((line, message))
    
    return issues


def _resolve_import_alias(name: str, base_dir: Path) -> Path | None:
    """
    Resolves an import name to a file path, or None if external.
    """
    parts = name.split('.')
    candidate = base_dir.joinpath(*parts)
    # Check for .py file
    py_file = candidate.with_suffix('.py')
    if py_file.exists():
        return py_file
    # Check for package __init__.py
    init_file = candidate / '__init__.py'
    if init_file.exists():
        return init_file
    # Not found: treat as external
    return None