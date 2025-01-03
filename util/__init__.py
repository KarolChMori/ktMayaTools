import importlib
# util/__init__.py
from . import kt_widgets

# Optionally, reload submodules to reflect any changes (useful in a development environment)
submodules = [kt_widgets]

for module in submodules:
    importlib.reload(module)