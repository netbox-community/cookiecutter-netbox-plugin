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

    display_attrs = ()          # Fields to show in results

indexes = (
    {{ cookiecutter.__model_name }}Index,
)
```

## Field Weights

The `fields` attribute defines which model fields are searchable and their relative importance. Higher weights mean higher priority in search results.

### Standard Weight Guidelines

NetBox uses standardized weights for consistency:

| Weight | Purpose | Examples |
|--------|---------|----------|
| **50** | Unique serialized attribute | Asset tag, serial number |
| **60** | Unique per related object | Device serial |
| **100** | Primary human identifier | Name, circuit ID |
| **110** | Slug fields | URL-safe identifiers |
| **200** | Secondary identifier | Account number |
| **300** | Highly unique descriptive text | Cross-connect ID |
| **500** | Description field | General descriptions |
| **1000** | Custom field (default) | User-defined fields |
| **2000** | Other discrete attributes | Port speed, VLAN ID |
| **5000** | Comments field | Detailed comments |

### Example Usage

```python
fields = (
    ('serial', 60),           # Unique identifier
    ('name', 100),            # Primary name
    ('slug', 110),            # URL slug
    ('identifier', 200),      # Secondary ID
    ('description', 500),     # Description text
    ('comments', 5000),       # Detailed comments
)
```

## Display Attributes

The `display_attrs` tuple specifies which fields to show in search results. These fields are NOT indexed for search but help users identify the correct result.

```python
display_attrs = (
    'status',       # Show current status
    'tenant',       # Show tenant relationship
    'site',         # Show location
    'description',  # Show description
)
```

**Benefits:**
- Provides context for search results
- Automatically prefetches related objects (ForeignKeys)
- Helps users distinguish between similar results

## Custom Category

By default, search results are grouped by the app's verbose name. You can customize this:

```python
class MyModelIndex(SearchIndex):
    model = MyModel
    category = 'Custom Category'  # Custom grouping label
    fields = (...)
```

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

## Searchable Field Types

NetBox automatically determines field types, but you can see what's supported:

- **String fields** - CharField, TextField, etc.
- **Integer fields** - IntegerField, PositiveIntegerField, etc.
- **Float fields** - FloatField, DecimalField
- **IP addresses** - IPAddressField (special handling)
- **CIDR networks** - CIDRField (special handling)
- **Custom fields** - Automatically included based on search_weight

## Custom Fields

If your model supports NetBox custom fields, they're automatically included in search with a default weight of 1000. Users can configure:
- `search_weight` - Controls inclusion and priority (0 = not searchable)
- `search_type` - Specifies field type for search

## Testing Search

You can test your search implementation:

```python
from netbox.search import search_backend

# Search for objects
results = search_backend.search('query string', model=MyModel)

# Check cached values
from extras.models import CachedValue
cached = CachedValue.objects.filter(
    object_type=ContentType.objects.get_for_model(MyModel)
)
```

## Registration

The PluginConfig automatically discovers and registers your search indexes from the `indexes` tuple. No additional configuration is needed!

The registration happens when NetBox loads your plugin, making your models immediately searchable.

## Best Practices

1. **Use standard weights** - Follow the weight guidelines for consistency
2. **Keep fields relevant** - Only index fields users will actually search
3. **Add display attributes** - Help users identify results
4. **Test your search** - Verify results appear correctly
5. **Document custom categories** - If using custom grouping, document why
6. **Consider performance** - Don't index extremely long text fields unnecessarily
7. **Update on model changes** - Add search for new searchable fields

## Common Patterns

### Basic Name Search
```python
fields = (
    ('name', 100),
)
```

### Name + Description
```python
fields = (
    ('name', 100),
    ('description', 500),
)
```

### Full Text Search
```python
fields = (
    ('name', 100),
    ('slug', 110),
    ('description', 500),
    ('comments', 5000),
)
display_attrs = ('status', 'tenant', 'description')
```

### Identifier-Heavy Model
```python
fields = (
    ('serial', 60),
    ('name', 100),
    ('identifier', 200),
    ('alternate_id', 300),
)
display_attrs = ('status', 'type', 'serial')
```

## Troubleshooting

**"My model doesn't appear in search results"**
- Verify `search.py` exists and has an `indexes` tuple
- Check that your model is in the `indexes` tuple
- Ensure objects exist in the database
- Check NetBox logs for registration errors

**"Search results have wrong weight/order"**
- Review your field weights
- Ensure you're following the standard weight guidelines
- Consider if multiple fields are matching with different weights

**"Display attributes not showing"**
- Verify field names are correct
- Check that fields exist on the model
- For related objects, ensure they're not None

**"Custom fields not searchable"**
- Check custom field `search_weight` is > 0
- Verify custom field is assigned to your content type
- Ensure objects have custom field values

## Additional Resources

- [NetBox Search Documentation](https://docs.netbox.dev/en/stable/plugins/development/search/)
- [NetBox Search Backend](https://docs.netbox.dev/en/stable/development/search/)
- [Django Model Fields](https://docs.djangoproject.com/en/stable/ref/models/fields/)
