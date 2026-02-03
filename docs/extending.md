# Extending Your Plugin

Once you have your plugin working, you'll want to add features and customize it for your needs. This guide covers common extension scenarios.

## NetBox Plugin Development Resources

The NetBox documentation provides comprehensive guides on plugin development:

- **[Plugin Development Overview](https://netboxlabs.com/docs/netbox/plugins/development/)** - Core concepts and architecture
- **[Models](https://netboxlabs.com/docs/netbox/plugins/development/models/)** - Creating and configuring plugin models
- **[Adding Models](https://netboxlabs.com/docs/netbox/development/adding-models/)** - Detailed guide on model creation
- **[Extending Models](https://netboxlabs.com/docs/netbox/development/extending-models/)** - Advanced model customization
- **[Views](https://netboxlabs.com/docs/netbox/plugins/development/views/)** - Creating plugin views
- **[Forms](https://netboxlabs.com/docs/netbox/plugins/development/forms/)** - Building forms for data entry
- **[Tables](https://netboxlabs.com/docs/netbox/plugins/development/tables/)** - Displaying data in tables
- **[REST API](https://netboxlabs.com/docs/netbox/plugins/development/rest-api/)** - Adding REST API endpoints
- **[GraphQL](https://netboxlabs.com/docs/netbox/plugins/development/graphql/)** - Adding GraphQL support

## Common Extension Tasks

### Adding Model Fields

When you need to add fields to your existing model:

1. Edit `models.py` and add your fields to the model class
2. Generate migrations from your NetBox directory:
   ```bash
   python netbox/manage.py makemigrations your_plugin_name
   ```
3. Review the generated migration in `your_plugin/migrations/`
4. Apply the migration:
   ```bash
   python netbox/manage.py migrate
   ```
5. Update related components:
   - Add fields to `forms.py` if they should be user-editable
   - Add columns to `tables.py` if they should be displayed in list views
   - Update `filtersets.py` if users should be able to filter by these fields
   - Add to `api/serializers.py` if exposing via REST API

!!! warning "Migration Safety"
    Always review generated migrations before applying them, especially when modifying existing fields. Test migrations in a development environment first.

### Adding New Models

To add additional models to your plugin:

1. Define the model class in `models.py`
2. Create forms in `forms.py` for data entry
3. Add table definitions in `tables.py` for list views
4. Create views in `views.py` for CRUD operations
5. Add URL patterns in `urls.py`
6. Update `navigation.py` to add menu items
7. Add filtersets in `filtersets.py` for search functionality
8. Generate and apply migrations as described above

For detailed guidance, see [Adding Models](https://netboxlabs.com/docs/netbox/development/adding-models/) in the NetBox documentation.

### Customizing Views

The generated plugin uses NetBox's generic views. To customize:

- Override view methods to change behavior
- Add custom views for special functionality
- Customize templates in `templates/your_plugin/`

See [Views](https://netboxlabs.com/docs/netbox/plugins/development/views/) for details.

### Adding Business Logic

Put business logic in appropriate locations:

- **Model methods** - Logic specific to a single object
- **Model managers** - Custom querysets and database operations
- **Form validation** - Input validation in `forms.py`
- **View methods** - Request/response handling logic
- **Utilities** - Shared functions in a `utils.py` module

### Working with Relationships

NetBox models can relate to each other and to core NetBox models:

- **ForeignKey** - Many-to-one relationships
- **ManyToManyField** - Many-to-many relationships
- **GenericForeignKey** - Flexible relationships to multiple model types

See [Extending Models](https://netboxlabs.com/docs/netbox/development/extending-models/) for examples.

### Adding Custom Fields and Tags

If you used `NetBoxModel` as your base class, your models automatically support:

- **Custom Fields** - User-defined fields via NetBox UI
- **Tags** - Organizing and filtering objects
- **Change Logging** - Automatic change tracking

No additional code needed - these features work out of the box!

## Testing Your Changes

After making changes:

1. Write tests for new functionality in `tests/`
2. Run your test suite:
   ```bash
   python netbox/manage.py test your_plugin.tests --parallel -v2
   ```
3. Use pre-commit hooks to check code quality:
   ```bash
   pre-commit run --all-files
   ```

See your plugin's `TESTING.md` for the complete testing guide.

## Best Practices

- **Follow NetBox patterns** - Study how core NetBox features are implemented
- **Keep it simple** - Don't over-engineer solutions
- **Test thoroughly** - Write tests for new features
- **Document changes** - Update docstrings and comments
- **Use type hints** - Makes code more maintainable
- **Follow PEP 8** - Use the included linting tools

## Getting Help

- **[NetBox Discussion Forum](https://github.com/netbox-community/netbox/discussions)** - Ask questions
- **[NetBox Slack](https://netdev.chat/)** - Real-time help (#netbox channel)
- **[Plugin Development Guide](https://netboxlabs.com/docs/netbox/plugins/development/)** - Official documentation

## Next Steps

Ready to share your plugin? See the [Publishing Guide](publishing.md).
