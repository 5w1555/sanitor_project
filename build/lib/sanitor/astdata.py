import ast
from typing import List
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

@dataclass
class ASTData:
    functions: List[ast.FunctionDef] = field(default_factory=list)
    constants: List[ast.Constant]    = field(default_factory=list)
    classes:   List[ast.ClassDef]    = field(default_factory=list)
    file_trees: Dict[Path, ast.AST]   = field(default_factory=dict)
