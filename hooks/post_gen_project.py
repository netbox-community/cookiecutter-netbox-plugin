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
        remove_dir("{{ cookiecutter.underscored }}/api")

    if "no" == "{{ cookiecutter.include_graphql }}":
        remove_file("{{ cookiecutter.underscored }}/graphql.py")
