# Cookiecutter NetBox Plugin

Cookiecutter template for a NetBox plugin, built with popular develop tools and
conform to best practice.

* Documentation: <https://netbox-community.github.io/cookiecutter-netbox-plugin/>
* Latest changes: [CHANGELOG.md](CHANGELOG.md)

**Note:** Plugins from this version target NetBox 4.5+

## Quickstart

Install the latest Cookiecutter if you haven't installed it yet (this requires Cookiecutter 2.6.0 or higher):

```
pip install -U cookiecutter
```

Generate a Python package project:

```
cookiecutter https://github.com/netbox-community/cookiecutter-netbox-plugin.git
```

Then follow the **[Quickstart Guide](docs/quickstart.md)** to finish other configurations.

## Features

This tool will create Python project with the following features:

* [Mkdocs](https://www.mkdocs.org): Writing your docs in markdown style
* Lint and format with [Ruff](https://github.com/astral-sh/ruff): Fast Python linter and formatter
* [Pre-commit hooks](https://pre-commit.com/): Automatic code quality checks on commit
* [Mkdocstrings](https://mkdocstrings.github.io/): Auto API doc generation
* Continuous Integration/Deployment by [GitHub actions](https://github.com/features/actions), includes:
    - Automated testing on every push
    - Publish documentation automatically
    - PyPI publishing with trusted publishers
* Host your documentation from [GitHub Pages](https://pages.github.com) with zero-config
