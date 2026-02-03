{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
* Documentation: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.hyphenated | replace("_", "-") }}/
{% endif %}

## Features

The features the plugin provides should be listed here. For example:

- Manage {{ cookiecutter.plugin_name }} resources through NetBox UI
- Track and organize {{ cookiecutter.plugin_name }} data with custom fields and tags
{% if cookiecutter.include_rest_api == "yes" -%}
- REST API endpoints for programmatic access
{% endif -%}
{% if cookiecutter.include_graphql == "yes" -%}
- GraphQL support for flexible data queries
{% endif -%}
- Full change logging and journaling support
- Integration with NetBox's permission system
- Global search integration for finding {{ cookiecutter.plugin_name }} objects
- Comprehensive filtering and table views

## Screenshots

<!-- Add screenshots or GIFs demonstrating your plugin's functionality here -->
_Screenshots will be added as features are developed._

## Compatibility

This plugin requires **NetBox 4.5** or later.

| NetBox Version | Plugin Version |
|----------------|----------------|
|     4.5+       |      0.1.0     |

For more detailed compatibility information, see [COMPATIBILITY.md](COMPATIBILITY.md).

## Dependencies

This plugin requires:
- NetBox {{ cookiecutter.version }} or later (NetBox 4.5+)
- Python 3.12 or later

No additional Python packages are required beyond NetBox's core dependencies.
{% if cookiecutter.include_rest_api == "yes" %}
## REST API

This plugin provides a REST API endpoint for managing {{ cookiecutter.plugin_name }} resources:

- `/api/plugins/{{ cookiecutter.underscored }}/{{ cookiecutter.__model_url }}s/` - List and create {{ cookiecutter.__model_name }} objects
{% endif %}
{% if cookiecutter.include_graphql == "yes" %}
## GraphQL

This plugin provides GraphQL support for querying {{ cookiecutter.plugin_name }} resources through NetBox's GraphQL API.
{% endif %}

## Installing

For adding to a NetBox Docker setup see
[the general instructions for using netbox-docker with plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins).

While this is still in development and not yet on pypi you can install with pip:

```bash
pip install git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.hyphenated }}
```

or by adding to your `local_requirements.txt` or `plugin_requirements.txt` (netbox-docker):

```bash
git+https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.hyphenated }}
```

Enable the plugin in `/opt/netbox/netbox/netbox/configuration.py`,
 or if you use netbox-docker, your `/configuration/plugins.py` file :

```python
PLUGINS = [
    '{{ cookiecutter.underscored }}'
]

PLUGINS_CONFIG = {
    "{{ cookiecutter.underscored }}": {},
}
```

## Configuration

This plugin does not require any additional configuration by default. Optional configuration parameters can be added to `PLUGINS_CONFIG` in your NetBox configuration file as needed.

## Usage

For detailed usage instructions, please refer to the [documentation](https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.hyphenated | replace("_", "-") }}/).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Reporting Bugs

Please report bugs by opening an issue on our [GitHub Issues](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.hyphenated }}/issues) page. When reporting bugs, please include:

- NetBox version
- Plugin version
- Python version
- Steps to reproduce
- Expected behavior
- Actual behavior

### Feature Requests

Feature requests can be submitted as [GitHub Issues](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.hyphenated }}/issues) with the "enhancement" label.

## Support

- **Documentation**: https://{{ cookiecutter.github_username }}.github.io/{{ cookiecutter.hyphenated | replace("_", "-") }}/
- **Issues**: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.hyphenated }}/issues
- **Discussions**: https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.hyphenated }}/discussions
- **NetBox Community Slack**: [netdev-community.slack.com](https://netdev.chat/)

## Credits

Based on the NetBox plugin tutorial:

- [demo repository](https://github.com/netbox-community/netbox-plugin-demo)
- [tutorial](https://github.com/netbox-community/netbox-plugin-tutorial)

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`netbox-community/cookiecutter-netbox-plugin`](https://github.com/netbox-community/cookiecutter-netbox-plugin) project template.
