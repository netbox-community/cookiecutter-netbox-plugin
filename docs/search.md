# Search Integration

The cookiecutter template includes a pre-configured `search.py` module that integrates your plugin's models with NetBox's global search functionality.

## What is NetBox Search?

NetBox provides a powerful global search feature accessible from the navigation bar. When users type a query, NetBox searches across all registered models and returns weighted results.

Your plugin's models can participate in this global search by defining search indexes.

## Generated Search Template

The template creates `{{ cookiecutter.underscored }}/search.py` with a basic search index for your primary model:

```python
from netbox.search import SearchIndex
from .models import {{ cookiecutter.__model_name }}

class {{ cookiecutter.__model_name }}Index(SearchIndex):
    model = {{ cookiecutter.__model_name }}

    fields = (
        ('name', 100),          # Primary identifier
    )

indexes = (
    {{ cookiecutter.__model_name }}Index,
)
```

## Configuring Search

The `fields` attribute defines which model fields are searchable and their relative importance. Higher weights mean higher priority in search results.

For detailed information on field weights, display attributes, custom categories, and other search configuration options, see the [NetBox Search Documentation](https://netboxlabs.com/docs/netbox/development/search/).

**Key topics in the NetBox documentation:**
- [Field Weight Guidance](https://netboxlabs.com/docs/netbox/development/search/#field-weight-guidance)
- [Display Attributes](https://netboxlabs.com/docs/netbox/development/search/#display-attributes)
- [Custom Categories](https://netboxlabs.com/docs/netbox/development/search/#custom-category)
- [Searchable Field Types](https://netboxlabs.com/docs/netbox/development/search/#searchable-field-types)

## Multiple Models

To make multiple models searchable, define an index for each and include all in the `indexes` tuple:

```python
class PrimaryModelIndex(SearchIndex):
    model = PrimaryModel
    fields = (
        ('name', 100),
        ('description', 500),
    )

class SecondaryModelIndex(SearchIndex):
    model = SecondaryModel
    fields = (
        ('name', 100),
        ('identifier', 200),
    )

indexes = (
    PrimaryModelIndex,
    SecondaryModelIndex,
)
```

## Registration

The PluginConfig automatically discovers and registers your search indexes from the `indexes` tuple. No additional configuration is needed!

The registration happens when NetBox loads your plugin, making your models immediately searchable.
