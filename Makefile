venv_dir = .venv
venv_activate = . $(venv_dir)/bin/activate

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

install: venv_setup poetry_install ## Setup Python and install dependencies
	poetry install

venv_setup: ## Setup Python virtual environment
	python3.9 -m venv $(venv_dir)

poetry_install: ## Install Poetry
	curl -sSL https://install.python-poetry.org | python3 -

run: ## Run app
	poetry run uvicorn main:app --reload

black: ## Check Python code formatting
	poetry run black --check --verbose .

pyright: ## Check Python code static tyoes
	poetry run pyright --stats .

bandit: ## Check Python code security
	poetry run bandit -c pyproject.toml -r .

flake: ## Check Python code style
	poetry run flake8 . -v

lint: black pyright bandit flake ## Run Python code checks

test: ## Run app tests
	poetry run pytest -vv --cov app

isort: ## Sort Python imports
	poetry run isort app/. tests/.

deploy-dev: ## Deploy app to dev
	poetry export -o requirements.txt --without-hashes
	deta deploy
	deta update --env .env
	deta visor enable
