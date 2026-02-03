# Changelog

## 0.3.0 (2026-02-03)

* Updates to target NetBox version 4.5.0

### New Features
* Optional REST API & GraphQL support via `include_rest_api` and `include_graphql` prompts
* Comprehensive testing infrastructure with base test classes and utilities
* Search template with `SearchIndex` class and documentation

### Improvements
* Ruff replaces Flake8 and Black for linting and formatting
* Updated pre-commit hooks configuration
* New documentation pages: testing.md, search.md
* Modern pyproject.toml format with setuptools >= 77.0.3

### Fixes
* Fixed NetBox 4.5 API compatibility (ObjectPermission, Token models)
* Fixed GraphQL schema configuration
* Fixed migrations directory structure

## 0.2.0 (2024-05-06)

* Updates to target NetBox 4.0.

## 0.1.0 (2023-02-06)

* First release on PyPI.
