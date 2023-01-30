# Cookiecutter NetBox Plugin

Cookiecutter template for a NetBox plugin, built with popular develop tools and
conform to best practice.

* Documentation: <https://netbox-community.github.io/cookiecutter-netbox-plugin/>

## Features

This tool will create Python project with the following features:

* [Mkdocs](https://www.mkdocs.org): Writing your docs in markdown style
* Format with [Black](https://github.com/psf/black) and [Isort](https://github.com/PyCQA/isort)
* Lint code with [Flake8](https://flake8.pycqa.org) and [Flake8-docstrings](https://pypi.org/project/flake8-docstrings/)
* [Pre-commit hooks](https://pre-commit.com/): Formatting/linting anytime when commit your code
* [Mkdocstrings](https://mkdocstrings.github.io/): Auto API doc generation
* Continuous Integration/Deployment by [GitHub actions](https://github.com/features/actions), includes:
    - publish documents automatically when CI success
    - extract changelog from CHANGELOG and integrate with release notes automatically
* Host your documentation from [GitHub Pages](https://pages.github.com) with zero-config

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this requires Cookiecutter 1.4.0 or higher):

```
pip install -U cookiecutter
```

Generate a Python package project:

```
cookiecutter https://github.com/netbox-community/cookiecutter-netbox-plugin.git
```

Then follow **[Tutorial](docs/tutorial.md)** to finish other configurations.
