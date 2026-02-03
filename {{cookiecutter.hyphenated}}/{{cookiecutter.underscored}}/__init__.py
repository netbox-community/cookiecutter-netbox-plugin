"""
{{ cookiecutter.project_name }}

Plugin configuration for {{ cookiecutter.project_name }}.

For a complete list of PluginConfig attributes, see:
https://docs.netbox.dev/en/stable/plugins/development/#pluginconfig-attributes
"""

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
    max_version = "4.5.99"
{%- if cookiecutter.include_graphql == "yes" %}
    graphql_schema = "graphql.schema"
{%- endif %}


config = {{ cookiecutter.__model_name }}Config
