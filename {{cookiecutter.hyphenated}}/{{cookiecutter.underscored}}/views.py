"""
Views for {{ cookiecutter.project_name }}.

For more information on NetBox views, see:
https://docs.netbox.dev/en/stable/plugins/development/views/

For generic view classes, see:
https://docs.netbox.dev/en/stable/development/views/
"""

from netbox.views import generic
from . import filtersets, forms, models, tables


class {{ cookiecutter.__model_name }}View(generic.ObjectView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()


class {{ cookiecutter.__model_name }}ListView(generic.ObjectListView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()
    table = tables.{{ cookiecutter.__model_name }}Table
    filterset = filtersets.{{ cookiecutter.__model_name }}FilterSet


class {{ cookiecutter.__model_name }}EditView(generic.ObjectEditView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()
    form = forms.{{ cookiecutter.__model_name }}Form


class {{ cookiecutter.__model_name }}DeleteView(generic.ObjectDeleteView):
    queryset = models.{{ cookiecutter.__model_name }}.objects.all()
