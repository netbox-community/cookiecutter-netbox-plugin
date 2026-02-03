"""
Forms for {{ cookiecutter.project_name }}.

For more information on NetBox forms, see:
https://docs.netbox.dev/en/stable/plugins/development/forms/
"""

from netbox.forms import NetBoxModelForm

from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Form(NetBoxModelForm):
    class Meta:
        model = {{ cookiecutter.__model_name }}
        fields = ("name", "tags")
