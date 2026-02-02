{% if cookiecutter.include_rest_api == "yes" -%}
"""
API URL patterns for {{ cookiecutter.project_name }}.

For more information on NetBox REST API routing, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#routers

For Django REST Framework routers, see:
https://www.django-rest-framework.org/api-guide/routers/
"""

from netbox.api.routers import NetBoxRouter
from .views import {{ cookiecutter.__model_name }}ViewSet


app_name = "{{ cookiecutter.underscored }}"

router = NetBoxRouter()
router.register("{{ cookiecutter.__model_url }}s", {{ cookiecutter.__model_name }}ViewSet)

urlpatterns = router.urls
{% endif %}
