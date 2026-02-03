"""
Search indexes for {{ cookiecutter.project_name }}.

This module defines search indexes to make plugin models searchable in NetBox's
global search. See: https://docs.netbox.dev/en/stable/plugins/development/search/
"""

from netbox.search import SearchIndex

from .models import {{ cookiecutter.__model_name }}


class {{ cookiecutter.__model_name }}Index(SearchIndex):
    """
    Search index for {{ cookiecutter.__model_name }} model.

    This enables {{ cookiecutter.__model_name }} objects to appear in NetBox's global
    search results.
    """

    model = {{ cookiecutter.__model_name }}

    # Fields to index for search with their weights
    # Higher weight = higher priority in search results
    #
    # Weight Guidelines:
    #   50   - Unique serialized attribute (e.g., asset_tag)
    #   60   - Unique per related object (e.g., serial)
    #   100  - Primary human identifier (e.g., name)
    #   110  - Slug fields
    #   200  - Secondary identifier
    #   300  - Highly unique descriptive text
    #   500  - Description field
    #   1000 - Custom field default
    #   2000 - Other discrete attributes
    #   5000 - Comments field
    fields = (
        ('name', 100),          # Primary identifier
        # ('slug', 110),        # Uncomment if your model has a slug field
        # ('description', 500), # Uncomment if your model has a description field
        # ('comments', 5000),   # Uncomment if your model has a comments field
    )

    # Optional: Fields to display in search results (not indexed, just shown)
    # These help users identify the correct result
    # Foreign key fields are automatically prefetched for efficiency
    display_attrs = (
        # 'status',      # Example: Display status
        # 'tenant',      # Example: Display tenant relationship
        # 'description', # Example: Display description
    )

    # Optional: Custom category label for grouping in search UI
    # If not specified, defaults to the app's verbose name
    # category = '{{ cookiecutter.project_name }}'


# Register all search indexes for this plugin
# The PluginConfig will automatically load these indexes
indexes = (
    {{ cookiecutter.__model_name }}Index,
)


# Example: Multiple models with different search configurations
#
# class AnotherModelIndex(SearchIndex):
#     """Search index for another model."""
#     model = AnotherModel
#     fields = (
#         ('name', 100),
#         ('identifier', 200),
#         ('description', 500),
#     )
#     display_attrs = ('status', 'type')
#
# indexes = (
#     {{ cookiecutter.__model_name }}Index,
#     AnotherModelIndex,
# )
