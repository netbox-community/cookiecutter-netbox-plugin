"""Top-level package for {{ cookiecutter.project_name }}."""

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = "{{ cookiecutter.email }}"
__version__ = "{{ cookiecutter.version }}"


from netbox.plugins import PluginConfig


class {{ cookiecutter.__model_name }}Config(PluginConfig):
    name = "{{ cookiecutter.underscored }}"
    verbose_name = "{{ cookiecutter.project_name }}"
    description = "{{ cookiecutter.project_short_description }}"
    version = "version"
    base_url = "{{ cookiecutter.underscored }}"


config = {{ cookiecutter.__model_name }}Config
