import sys, os
from pathlib import Path
try:
    import httpx
    httpx_ver = httpx.__version__
except Exception as e:
    httpx_ver = f"not installed ({e})"
print("=== Project: py312 ===")
print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Venv active:", bool(os.environ.get("VIRTUAL_ENV")))
print("httpx:", httpx_ver)
print("CWD:", Path.cwd())
