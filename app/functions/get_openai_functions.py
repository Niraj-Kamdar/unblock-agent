from functools import lru_cache


@lru_cache(maxsize=1)
def get_functions():
    from .covalent import covalent
    from .general import general
    from .safe import safe
    from .system import system

    fns = [*covalent, *general, *safe, *system]
    return {fn["_id"]: fn for fn in fns}
