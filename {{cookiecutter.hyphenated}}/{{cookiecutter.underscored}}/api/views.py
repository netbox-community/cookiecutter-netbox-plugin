{% if cookiecutter.include_rest_api == "yes" -%}
from netbox.api.viewsets import NetBoxModelViewSet

from ..models import {{ cookiecutter.__model_name }}
from .serializers import {{ cookiecutter.__model_name }}Serializer


class {{ cookiecutter.__model_name }}ViewSet(NetBoxModelViewSet):
    queryset = {{ cookiecutter.__model_name }}.objects.all()
    serializer_class = {{ cookiecutter.__model_name }}Serializer
{% endif %}
