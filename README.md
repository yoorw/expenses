# Expenses project

Short notes to get this project running locally using pipenv and pyenv on macOS (zsh).

## Required Python

- This project expects Python 3.12 (full version 3.12.11).
- The repository `Pipfile` contains:

```
[requires]
python_version = "3.12"
python_full_version = "3.12.11"
```

If you use `pyenv`, ensure `3.12.11` is installed and activated for the project (see commands below).

## Quick setup (recommended)

Run these commands from a zsh shell inside the project directory :

```bash
# 1) Ensure pyenv has the required Python version installed
pyenv install --skip-existing 3.12.11

# 2) Make 3.12.11 the local python for this project
pyenv local 3.12.11

# 3) Install pipenv (if you don't already have it)
# Option A: using pip (user install avoids system perms)
python3 -m pip install --user pipenv
# Option B: using Homebrew (preferred for macOS users who use brew)
# brew install pipenv

# 4) Create the pipenv environment using the activated pyenv python
pipenv --python 3.12.11

# 5) Install dependencies listed in Pipfile (if not already installed)
pipenv install --dev

# 6) Open a project shell or run commands inside the venv
pipenv shell        # interactive shell inside the venv
# or run single commands without activating shell
pipenv run python -V
pipenv run pytest
```

Notes:
- If `pipenv --python 3.12.11` still picks the wrong interpreter, pass the full pyenv path:
  ```bash
  pipenv --python "$(pyenv prefix 3.12.11)/bin/python"
  ```
- To recreate the virtualenv if pipenv already created one with the wrong Python:
  ```bash
  pipenv --rm       # remove existing venv
  pipenv --clear    # clear caches if needed
  pipenv --python 3.12.11
  ```

## Verify the environment

```bash
pipenv --venv          # prints venv path
pipenv run python -V   # should print Python 3.12.11
pipenv graph           # show installed packages
cat Pipfile            # confirm [requires] section
```

## How to run tests

Install dev dependencies (if not already):
```bash
pipenv install --dev
```

Run tests:
```bash
pipenv run pytest
```

## Useful tips

- If you prefer the virtualenv to live inside the project directory (visible `.venv/`), enable it before creating the venv:
  ```bash
  export PIPENV_VENV_IN_PROJECT=1
  pipenv --python 3.12.11
  ```
- If `pipenv` is not found after installing with `pip --user`, ensure your user bin is in PATH (for zsh typically `~/.local/bin` or `~/.pyenv/shims`).
- For CI use: prefer installing from `Pipfile.lock` with `pipenv install --deploy --ignore-pipfile` for deterministic builds.

## Troubleshooting

- If `python -V` shows a different version than expected after `pyenv local`, ensure your shell initialisation loads pyenv shims (in `~/.zshrc`):
  ```bash
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)"
  ```
- If pipenv created a Pipfile with an older version, updating/removing the venv and re-running `pipenv --python` as above will fix it.

## Files of interest

- `Pipfile` — lists required Python and dependencies.
- `Pipfile.lock` — exact dependency snapshot (use in CI).

