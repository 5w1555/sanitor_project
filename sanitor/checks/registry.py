def register(name=None, severity=None):
    def decorator(fn):
        fn._check_name = name
        fn._severity = severity
        return fn
    return decorator
