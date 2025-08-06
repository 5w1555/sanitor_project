# sanitor/checks/large_classes.py
import ast
from sanitor.engine import ASTData

def check_large_classes(data: ASTData, cfg: dict):
    """
    Flag classes with too many public methods.
    """
    max_methods = cfg.get("max_methods", 12)
    issues = []
    
    for cls in data.classes:
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
        public = [m for m in methods if not m.name.startswith('_')]
        count = len(public)
        if count > max_methods:
            issues.append((
                cls.lineno,
                f"Large class '{cls.name}' has {count} public methods - consider splitting"
            ))
    return issues
