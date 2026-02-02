from netbox.forms import NetBoxModelForm

from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Form(NetBoxModelForm):
    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = ("name", "tags")
