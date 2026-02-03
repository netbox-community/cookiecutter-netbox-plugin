"""
Filtersets for {{ cookiecutter.project_name }}.

For more information on NetBox filtersets, see:
https://docs.netbox.dev/en/stable/plugins/development/filtersets/

For django-filters documentation, see:
https://django-filter.readthedocs.io/
"""

from netbox.filtersets import NetBoxModelFilterSet

from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}FilterSet(NetBoxModelFilterSet):
    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = ("id", "name")

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
