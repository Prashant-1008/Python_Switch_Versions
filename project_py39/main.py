import sys, os
from pathlib import Path
try:
    import requests
    req_ver = requests.__version__
except Exception as e:
    req_ver = f"not installed ({e})"
print("=== Project: py39 ===")
print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Venv active:", bool(os.environ.get("VIRTUAL_ENV")))
print("requests:", req_ver)
print("CWD:", Path.cwd())
