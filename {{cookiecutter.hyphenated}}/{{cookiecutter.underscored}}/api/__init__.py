"""
{% if cookiecutter.include_rest_api == "yes" -%}
REST API for {{ cookiecutter.project_name }}.

For more information on developing NetBox REST APIs, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/
{%- else -%}
API serializers for {{ cookiecutter.project_name }}.

Serializers are required for NetBox event handling (webhooks, change logging).
REST API endpoints are disabled for this plugin.
{%- endif %}
"""
