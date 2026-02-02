{% if cookiecutter.include_rest_api == "yes" -%}
from netbox.api.routers import NetBoxRouter
from .views import {{ cookiecutter.__model_name }}ViewSet


app_name = "{{ cookiecutter.underscored }}"

router = NetBoxRouter()
router.register("{{ cookiecutter.__model_url }}s", {{ cookiecutter.__model_name }}ViewSet)

urlpatterns = router.urls
{% endif %}
