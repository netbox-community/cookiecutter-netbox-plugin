sources = {{ cookiecutter.underscored }}

.PHONY: test format lint unittest pre-commit clean
test: format lint unittest

format:
	ruff check --select I --fix $(sources) tests
	ruff format $(sources) tests

lint:
	ruff check $(sources) tests

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf *.egg-info
	rm -rf .tox dist site
