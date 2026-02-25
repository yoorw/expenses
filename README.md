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

### Prerequisites 
1. pipenv 
    - Mac OS:
        - ```brew install pipenv``` 

2. pyenv (to set up Python Version)
   - Mac OS:
        - `brew install pyenv` 
        - [Go to Python Setup for Python version install](#python-install-using-pyenv)

### Setup
1. Start Virtual Environment
   - `pipenv shell`
2. Install Dependencies / Packages 
   - `pipenv install --dev` 

### Run Unit Tests 
`pipenv run pytest expenses/`

### Run Application
`pipenv run python main.py`


## Python Install Using Pyenv

```bash
# 1) Use pyenv to install the required Python version 
pyenv install --skip-existing 3.12.11

# 2) Make 3.12.11 the local python for this project
pyenv local 3.12.11

# 3) Create the pipenv environment using the activated pyenv python
pipenv --python 3.12.11
```


