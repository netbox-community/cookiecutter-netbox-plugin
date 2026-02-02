{% if cookiecutter.include_graphql == "yes" -%}
"""
GraphQL schema for {{ cookiecutter.project_name }}.

For more information on NetBox GraphQL, see:
https://docs.netbox.dev/en/stable/plugins/development/graphql/

For Graphene (GraphQL library) documentation, see:
https://docs.graphene-python.org/
"""

import graphene
from netbox.graphql.types import NetBoxObjectType

from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Type(NetBoxObjectType):
    """GraphQL type for {{ cookiecutter.__model_name }} model."""

    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = "__all__"


class Query(graphene.ObjectType):
    """GraphQL queries for {{ cookiecutter.project_name }}."""

    {{ cookiecutter.__model_url_name }} = graphene.Field({{ cookiecutter.__model_name }}Type, id=graphene.Int())
    {{ cookiecutter.__model_url_name }}_list = graphene.List({{ cookiecutter.__model_name }}Type)

    def resolve_{{ cookiecutter.__model_url_name }}(self, info, id):
        return {{ cookiecutter.__model_name }}.objects.get(pk=id)

    def resolve_{{ cookiecutter.__model_url_name }}_list(self, info):
        return {{ cookiecutter.__model_name }}.objects.all()


schema = graphene.Schema(query=Query)
{% endif %}
