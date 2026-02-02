"""Top-level package for {{ cookiecutter.project_name }}."""

__author__ = """{{ cookiecutter.full_name }}"""
__email__ = "{{ cookiecutter.email }}"
__version__ = "{{ cookiecutter.version }}"


from netbox.plugins import PluginConfig


class {{ cookiecutter.__model_name }}Config(PluginConfig):
    name = "{{ cookiecutter.underscored }}"
    verbose_name = "{{ cookiecutter.project_name }}"
    description = "{{ cookiecutter.project_short_description }}"
    author= "{{ cookiecutter.full_name }}"
    author_email = "{{ cookiecutter.email }}"
    version = __version__
    base_url = "{{ cookiecutter.underscored }}"
    min_version = "4.5.0"
    max_version = "4.9.999"
{% if cookiecutter.include_graphql == "yes" -%}
    graphql_schema = "{{ cookiecutter.underscored }}.graphql.schema"
{% endif %}


config = {{ cookiecutter.__model_name }}Config
