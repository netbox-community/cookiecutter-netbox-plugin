#!/usr/bin/env python
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    to_remove = os.path.join(PROJECT_DIRECTORY, filepath)
    if os.path.isfile(to_remove):
        os.remove(os.path.join(PROJECT_DIRECTORY, filepath))
    else:
        shutil.rmtree(to_remove)



if __name__ == '__main__':

    if 'Not open source' == '{{ cookiecutter.open_source_license }}':
        remove_file('LICENSE')
    if 'True' != '{{ cookiecutter.devcontainer }}':
        remove_file('.devcontainer/')