{% if cookiecutter.include_rest_api == "yes" -%}
from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer

from ..models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Serializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:{{ cookiecutter.underscored }}-api:{{ cookiecutter.__model_url_name }}-detail"
    )

    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = ("id", "url", "display", "name", "tags", "custom_fields", "created", "last_updated")
{% endif %}
