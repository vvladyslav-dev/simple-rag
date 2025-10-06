from core.container import Container
from presentation.ui import run_app
import core.usecases as usecases_pkg
import importlib
import pkgutil

def _import_all_submodules(package):
    for m in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        importlib.import_module(m.name)

def main():
    _import_all_submodules(usecases_pkg)

    container = Container()
    container.wire(packages=[usecases_pkg])

    run_app()

if __name__ == "__main__":
    main()
