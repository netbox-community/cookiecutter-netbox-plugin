#!/usr/bin/env python
from __future__ import annotations

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(dirpath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))


if __name__ == "__main__":
    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    if "no" == "{{ cookiecutter.include_rest_api }}":
        # Keep api/ directory and serializers.py (required for NetBox events)
        # but remove REST API views and URLs
        remove_file("{{ cookiecutter.underscored }}/api/views.py")
        remove_file("{{ cookiecutter.underscored }}/api/urls.py")
        remove_file("{{ cookiecutter.underscored }}/tests/test_api.py")

    if "no" == "{{ cookiecutter.include_graphql }}":
        remove_file("{{ cookiecutter.underscored }}/graphql.py")
        remove_file("{{ cookiecutter.underscored }}/tests/test_graphql.py")
