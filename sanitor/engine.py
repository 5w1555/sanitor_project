# sanitor/engine.py

import ast
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, field

# Pull ASTData from its own module (no circular here)
from sanitor.astdata import ASTData

@dataclass
class Issue:
    file: Path
    line: int
    code: str
    severity: str
    message: str

def collect_ast_data(tree: ast.AST) -> ASTData:
    data = ASTData()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            data.functions.append(node)
        elif isinstance(node, ast.Constant):
            data.constants.append(node)
        elif isinstance(node, ast.ClassDef):
            data.classes.append(node)
    return data

def run_checks(path: Path, config: Dict[str, Any]) -> List[Issue]:
    # Lazy-import checks to avoid circular import at module load time
    from sanitor.checks import CHECKS

    source = path.read_text(encoding="utf-8")
    tree   = ast.parse(source, filename=str(path))
    data   = collect_ast_data(tree)
    # Collect nodes into data.functions, data.constants, data.classes
    data.file_trees[path] = tree

    issues: List[Issue] = []
    for code, check_fn in CHECKS.items():
        params = config.get(code, {})
        for line, msg in check_fn(data, params):
            issues.append(Issue(
                file=path,
                line=line,
                code=code,
                severity=params.get("severity", "medium"),
                message=msg
            ))
    return issues
