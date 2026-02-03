{% if cookiecutter.include_rest_api == "yes" -%}
"""
API viewsets for {{ cookiecutter.project_name }}.

For more information on NetBox REST API viewsets, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#viewsets

For Django REST Framework viewsets, see:
https://www.django-rest-framework.org/api-guide/viewsets/
"""

from netbox.api.viewsets import NetBoxModelViewSet

from ..models import {{ cookiecutter.__model_name }}
from .serializers import {{ cookiecutter.__model_name }}Serializer


class {{ cookiecutter.__model_name }}ViewSet(NetBoxModelViewSet):
    queryset = {{ cookiecutter.__model_name }}.objects.all()
    serializer_class = {{ cookiecutter.__model_name }}Serializer
{% endif %}
