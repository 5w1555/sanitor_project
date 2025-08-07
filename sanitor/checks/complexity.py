import ast
from sanitor.astdata import ASTData

def check_complexity(data: ASTData, cfg: dict):
    """
    Compute McCabe cyclomatic complexity per function.
    """
    max_complexity = cfg.get("max_complexity", 20)
    issues = []
    
    for fn in data.functions:
        complexity = 1
        for node in ast.walk(fn):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.AsyncFor,
                                 ast.With, ast.AsyncWith, ast.ExceptHandler,
                                 ast.Assert)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.comprehension):
                complexity += len(node.ifs)
        if complexity > max_complexity:
            issues.append((
                fn.lineno,
                f"Function '{fn.name}' has high cyclomatic complexity ({complexity}), exceeds limit of {max_complexity}."
            ))
    return issues
