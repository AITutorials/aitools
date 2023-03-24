import os
import sys
import importlib

def get_config_from_filename(path, name):
    filename = os.path.join(path, name)
    sys.path.append(path)
    if not os.path.exists(filename):
        raise RuntimeError("%r doesn't exist" % filename)
    ext = os.path.splitext(filename)[1]
    module_name = '__config__'
    if ext in [".py", ".pyc"]:
        spec = importlib.util.spec_from_file_location(module_name, filename)
    else:
        msg = "configuration file should have a valid Python extension.\n"
        util.warn(msg)
        loader_ = importlib.machinery.SourceFileLoader(module_name, filename)
        spec = importlib.util.spec_from_file_location(module_name, filename, loader=loader_)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return vars(mod)
