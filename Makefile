venv_dir = .venv
venv_activate = . $(venv_dir)/bin/activate

install: venv_setup poetry_install
	poetry install

venv_setup:
	python3.10 -m venv $(venv_dir)

poetry_install:
	curl -sSL https://install.python-poetry.org | python3 -

run:
	@echo "Run target in Makefile not configured."

black:
	poetry run black --check --verbose .

pyright:
	poetry run pyright --stats .

bandit:
	poetry run bandit -c pyproject.toml -r .

flake:
	poetry run flake8 . -v

lint: black pyright bandit flake

test:
	poetry run pytest -v
