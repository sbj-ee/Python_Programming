# Dynamic Loading

Python imports are already fairly dynamic — `import` is a runtime statement,
not a compile-time directive. `importlib` exposes that machinery directly,
enabling plugin architectures: load code by name, discovered at runtime,
without the importer knowing what it is in advance.

## importlib.import_module: import by string name

```python
import importlib

module_name = "json"                       # could come from a config file
module = importlib.import_module(module_name)
module.dumps({"a": 1})

# equivalent to `import json`, but the name is a runtime string
plugin_name = config["plugin"]              # e.g. "plugins.csv_exporter"
plugin = importlib.import_module(plugin_name)
```

## A minimal plugin pattern

```python
import importlib
import pkgutil

def load_plugins(package_name: str) -> dict:
    """Discover and import every module in a package, collecting
    whatever each one registers.
    """
    plugins = {}
    package = importlib.import_module(package_name)
    for _finder, name, _is_pkg in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{name}")
        if hasattr(module, "register"):
            plugins[name] = module.register()
    return plugins
```

```python
# plugins/csv_exporter.py
def register():
    return {"format": "csv", "export": export_csv}
```

## Entry points: the packaging-level plugin mechanism

```python
# In a package's pyproject.toml:
# [project.entry-points."myapp.plugins"]
# csv = "myapp_csv_plugin:register"

from importlib.metadata import entry_points

for ep in entry_points(group="myapp.plugins"):
    plugin_factory = ep.load()      # imports and returns the referenced object
    plugin_factory()
```

Entry points let independently-installed packages register plugins with an
application without either side importing the other directly — the
mechanism behind pytest plugins, Flask extensions, and many CLI tool
ecosystems.

## __import__ and reload

```python
mod = __import__("os")     # the low-level function import statements compile to;
                              # importlib.import_module() is the preferred API

importlib.reload(module)    # re-executes a module's top-level code --
                              # useful in interactive/dev workflows, risky elsewhere
                              # (old references to replaced classes/functions
                              # from before the reload keep pointing at the OLD code)
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Importing untrusted plugin code without sandboxing | Arbitrary code execution -- the module's top level runs on import | Only load plugins from trusted sources; consider subprocess isolation for untrusted code |
| Using `importlib.reload()` in production logic | Stale references to pre-reload classes/functions cause subtle bugs | Reserve `reload()` for interactive development only |
| Assuming `import_module("pkg.sub")` also binds `pkg` and `pkg.sub` as if written statically | Actually it does register both in `sys.modules`, but local names still need explicit assignment | Capture the return value; don't rely on implicit local bindings |
| Building a plugin system without a clear registration contract | Plugins silently fail to load if they don't match the expected shape | Define and document a stable `register()`/entry-point contract, validate on load |
| Circular plugin imports (plugin imports the app, which imports the plugin) | `ImportError` at load time | Keep the shared contract (interfaces/protocols) in a separate module both sides import |
