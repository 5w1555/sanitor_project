from .magic_numbers       import check_magic_numbers
from .duplicate_structure import check_duplicate_structure
from .vague_naming        import check_vague_naming
from .similar_names       import check_similar_functions
from .large_classes       import check_large_classes
from .complexity          import check_complexity
from .import_cycles       import check_import_cycles

CHECKS = {
    'magic_numbers':       check_magic_numbers,
    'duplicate_structure': check_duplicate_structure,
    'vague_naming':        check_vague_naming,
    'similar_names':       check_similar_functions,
    'large_classes':       check_large_classes,
    'complexity':          check_complexity,
    'import_cycles':       check_import_cycles
}