"""
Tables for {{ cookiecutter.project_name }}.

For more information on NetBox tables, see:
https://docs.netbox.dev/en/stable/plugins/development/tables/

For django-tables2 documentation, see:
https://django-tables2.readthedocs.io/
"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, ChoiceFieldColumn

from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Table(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = {{ cookiecutter.__model_name }}
        fields = ("pk", "id", "name", "actions")
        default_columns = ("name",)
