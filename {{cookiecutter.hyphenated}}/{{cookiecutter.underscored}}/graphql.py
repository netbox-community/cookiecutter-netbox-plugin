{% if cookiecutter.include_graphql == "yes" -%}
"""
GraphQL schema for {{ cookiecutter.project_name }}.

For more information on NetBox GraphQL, see:
https://docs.netbox.dev/en/stable/plugins/development/graphql/

For Strawberry GraphQL documentation, see:
https://strawberry.rocks/
"""

from typing import List

import strawberry
import strawberry_django

from .models import {{ cookiecutter.__model_name }}


@strawberry_django.type(
    {{ cookiecutter.__model_name }},
    fields='__all__',
)
class {{ cookiecutter.__model_name }}Type:
    """GraphQL type for {{ cookiecutter.__model_name }} model."""
    pass


@strawberry.type(name="Query")
class {{ cookiecutter.__model_name }}Query:
    """GraphQL queries for {{ cookiecutter.project_name }}."""

    {{ cookiecutter.__model_url_name }}: {{ cookiecutter.__model_name }}Type = strawberry_django.field()
    {{ cookiecutter.__model_url_name }}_list: List[{{ cookiecutter.__model_name }}Type] = strawberry_django.field()


schema = [
    {{ cookiecutter.__model_name }}Query,
]
{% endif %}
