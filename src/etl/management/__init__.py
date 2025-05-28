import importlib, pkgutil, etl.management as _pkg
for mod_info in pkgutil.iter_modules(_pkg.__path__):
    importlib.import_module(f"{_pkg.__name__}.{mod_info.name}")