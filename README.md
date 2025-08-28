# Python Version Switching Demo (pyenv + venv)

This repo demonstrates clean switching between multiple Python versions using `pyenv`, with two sample projects:
- `project_py39` uses Python 3.9.19 with `requests`
- `project_py312` uses Python 3.12.5 with `httpx`

Each project can be run both ways:
- without a venv (using the `pyenv`-provided interpreter directly)
- with a per-project venv (`python -m venv .venv`)

## Prerequisites

- Linux (tested on Ubuntu 22.04)
- `pyenv` (installed to `~/.pyenv`) with build deps
- Shell initialization includes pyenv

If you need to install:
```bash
# Build tools and Python build dependencies (Ubuntu/Debian)
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends \
  build-essential curl git ca-certificates \
  libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libffi-dev liblzma-dev tk-dev uuid-dev

# Install pyenv and common plugins
curl https://pyenv.run | bash

# Add to ~/.bashrc (already done on this machine):
# export PYENV_ROOT="$HOME/.pyenv"
# [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init - bash)"
# eval "$(pyenv virtualenv-init -)"

# Reload shell
bash -lic 'pyenv --version'
```

## Install Python versions with pyenv

The demo uses these exact versions:
```bash
bash -lic 'pyenv install -s 3.9.19 && pyenv install -s 3.12.5'
```

## Project structure

```text
Task1/
  project_py39/
    .python-version          # set by: pyenv local 3.9.19
    requirements.txt         # requests, colorama
    main.py                  # prints versions and venv status
    .venv/                   # optional virtual environment (created on demand)
  project_py312/
    .python-version          # set by: pyenv local 3.12.5
    requirements.txt         # httpx, colorama
    main.py                  # prints versions and venv status
    .venv/                   # optional virtual environment (created on demand)
```

## What the scripts print

Each `main.py` prints:
- Project label
- Python version in use
- Executable path
- Whether a venv is active
- Package version (`requests` for 3.9 project, `httpx` for 3.12 project)

Example output without venv (pyenv only):
```text
=== Project: py39 ===
Python: 3.9.19
Executable: /home/<user>/.pyenv/versions/3.9.19/bin/python
Venv active: False
requests: 2.31.0
```

Example output with venv:
```text
=== Project: py312 ===
Python: 3.12.5
Executable: /path/to/project_py312/.venv/bin/python
Venv active: True
httpx: 0.27.2
```

## Run WITHOUT venv (pyenv only)

- 3.9 project:
```bash
cd project_py39
pyenv local 3.9.19
pip3 install -r requirements.txt
python main.py
```

- 3.12 project:
```bash
cd project_py312
pyenv local 3.12.5
pip3 install -r requirements.txt
python main.py
```

What this demonstrates:
- `pyenv local` pins the interpreter for the current directory via `.python-version`
- `python` resolves to the pyenv-managed interpreter, not system Python
- `Venv active: False` confirms no venv is activated

## Run WITH venv (isolated per-project)

- 3.9 project:
```bash
cd project_py39
pyenv local 3.9.19
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
# later
deactivate
```

- 3.12 project:
```bash
cd project_py312
pyenv local 3.12.5
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
# later
deactivate
```

What this demonstrates:
- venv is created using the pyenv-selected interpreter for that folder
- Executable path points inside `.venv/bin/python`
- `Venv active: True` confirms isolation

## Switching between 3.9 and 3.12

To show switching clearly during a demo:
```bash
cd project_py39 && python --version && which python && python main.py
cd ../project_py312 && python --version && which python && python main.py
```
You will see different Python versions and executables per directory.

## Project files (for reference)

`project_py39/requirements.txt`:
```text
requests==2.31.0
colorama==0.4.6
```

`project_py39/main.py`:
```python
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
```

`project_py312/requirements.txt`:
```text
httpx==0.27.2
colorama==0.4.6
```

`project_py312/main.py`:
```python
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
```

## Useful checks

- Which Python is active?
```bash
python --version
which python
```

- Which pyenv version is in a directory?
```bash
pyenv version
cat .python-version
```

- List installed Python versions (pyenv):
```bash
pyenv versions
```

## Troubleshooting

- `pyenv: command not found`
  - Ensure your `~/.bashrc` contains:
    ```bash
    export PYENV_ROOT="$HOME/.pyenv"
    [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init - bash)"
    eval "$(pyenv virtualenv-init -)"
    ```
  - Start a new shell: `bash -lic 'pyenv --version'`

- Build fails while installing a Python version
  - Re-check build deps (listed in Prerequisites)
  - Clean and retry: `rm -rf ~/.pyenv/sources/*` then `pyenv install <version>`

- Wrong Python used when activating venv
  - Always run `python -m venv .venv` after `pyenv local <version>`.
  - Verify with `which python` before creating the venv.

- Mixing global and local versions
  - Prefer using `.python-version` per project with `pyenv local`.
  - Check current resolution with `pyenv which python`.

## Optional: Make quick demo targets

You can add `Makefile` targets per project if you want one-liners like `make run-venv` or `make run-no-venv`. Ask and we’ll generate them. 