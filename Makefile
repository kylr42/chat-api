include .env
export

# enumeration of * .py files storage or folders is required.
files_to_fmt 	?= app server
files_to_check 	?= app server

# Sphinx settings
SPHINX_BUILD 	?= sphinx-build
SPHINX_TEMPLATES ?= ./docs/_templates
SOURCE_DIR     	= ./docs
BUILD_DIR      	= ./docs/_build


## Default target
.DEFAULT_GOAL := run

## Build api docker containers
docker_up:
	docker-compose up --build -d

run:
	uvicorn app:create_app --host localhost --reload --port ${API_SERVER_PORT}

# Build sphinx docs
docs: build_docs rst_builder
build_docs:
	: # Build *.rst from docstrings
	poetry run sphinx-apidoc -f -o "$(SOURCE_DIR)" . -t="$(SPHINX_TEMPLATES)"


rst_builder:
	: # Build html pages from *.rst
	poetry run $(SPHINX_BUILD) -b html "$(SOURCE_DIR)" "$(BUILD_DIR)"



## Format all
fmt: format
format: isort black docformatter add-trailing-comma


## Check code quality
chk: check
lint: check
check: flake8 black_check docformatter_check safety bandit

## Migrate database
migrate:
	poetry run python -m scripts.migrate

## Rollback migrations in database
migrate-rollback:
	poetry run python -m scripts.migrate --rollback --config ./config/yoyo.ini

migrate-reload:
	poetry run python -m scripts.migrate --reload --config ./config/yoyo.ini

## Sort imports
isort:
	poetry run isort ${files_to_fmt}


## Format code
black:
	poetry run black ${files_to_fmt}


## Check code formatting
black_check:
	poetry run black --check ${files_to_check}


## Format docstring PEP 257
docformatter:
	poetry run docformatter -ir ${files_to_fmt}


## Check docstring formatting
docformatter_check:
	poetry run docformatter -cr ${files_to_check}


## Check pep8
flake8:
	poetry run flake8 ${files_to_check} --config ./config/setup.cfg


## Check typing
mypy:
	poetry run mypy ${files_to_check} --config ./config/setup.cfg


## Check if all dependencies are secure and do not have any known vulnerabilities
safety:
	poetry run safety check --full-report


## Check code security
bandit:
	poetry run bandit -r ${files_to_check} -x app

## Add trailing comma works only on unix.
# an error is expected on windows.
add-trailing-comma:
	find app server -name "*.py" -exec poetry run add-trailing-comma '{}' --py36-plus \;
