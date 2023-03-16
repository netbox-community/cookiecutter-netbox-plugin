sources = {{ cookiecutter.project_name }}
{%- if cookiecutter.devcontainer == "True" -%}
PLUGIN_NAME={{ cookiecutter.project_slug }}
REPO_PATH=/opt/netbox/netbox/{{ cookiecutter.project_slug }}
VENV_PY_PATH=/opt/netbox/venv/bin/python3
NETBOX_MANAGE_PATH=/opt/netbox/netbox/manage.py
VERFILE=./version.py
{% endif %}


.PHONY: test format lint unittest pre-commit clean
test: format lint unittest

format:
	isort $(sources) tests
	black $(sources) tests

lint:
	flake8 $(sources) tests

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf *.egg-info
	rm -rf .tox dist site

{%- if cookiecutter.devcontainer == "True" -%}
.PHONY: nbshell ## Run nbshell
nbshell:
	${VENV_PY_PATH} ${NETBOX_MANAGE_PATH} nbshell
	from {{ cookiecutter.project_slug }}.models import *

.PHONY: setup ## Copy plugin settings.  Setup NetBox plugin.
setup:
	-${VENV_PY_PATH} -m pip install --disable-pip-version-check --no-cache-dir -e ${REPO_PATH}
#-python3 setup.py develop

.PHONY: example_initializers ## Run initializers
example_initializers:
	-${VENV_PY_PATH} ${NETBOX_MANAGE_PATH} copy_initializers_examples --path /opt/netbox/netbox/{{ cookiecutter.project_slug }}/.devcontainer/initializers

.PHONY: load_initializers ## Run initializers
load_initializers:
	-${VENV_PY_PATH} ${NETBOX_MANAGE_PATH} load_initializer_data  --path /opt/netbox/netbox/{{ cookiecutter.project_slug }}/.devcontainer/initializers

.PHONY: makemigrations ## Run makemigrations
makemigrations:
	-${VENV_PY_PATH} ${NETBOX_MANAGE_PATH} makemigrations --name ${PLUGIN_NAME}

.PHONY: migrate ## Run migrate
migrate:
	-${VENV_PY_PATH} ${NETBOX_MANAGE_PATH} migrate

.PHONY: startup_scripts
startup_scripts:
	-echo "import runpy; runpy.run_path('/opt/netbox/startup_scripts')" | ${NETBOX_MANAGE_PATH} shell --interface python

.PHONY: collectstatic
collectstatic:
	-${VENV_PY_PATH} ${NETBOX_MANAGE_PATH} collectstatic --no-input

.PHONY: start ## Start NetBox
start:
	- cd /opt/netbox/netbox/ && /opt/netbox/docker-entrypoint.sh && /opt/netbox/launch-netbox.sh

.PHONY: all ## Run all PLUGIN DEV targets
all: setup makemigrations migrate collectstatic start
{% endif %}