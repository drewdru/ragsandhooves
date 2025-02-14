import pkgutil
import importlib
from sqlmodel import SQLModel # noqa

package = __name__
for _, module_name, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{package}.{module_name}")
