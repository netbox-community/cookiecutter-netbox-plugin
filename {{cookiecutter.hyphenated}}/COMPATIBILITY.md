# Compatibility

This document tracks the minimum and maximum supported NetBox versions for each release of {{ cookiecutter.project_name }}.

| Plugin Version | Minimum NetBox Version | Maximum NetBox Version |
|----------------|------------------------|------------------------|
| {{ cookiecutter.version }} | 4.5.0 | 4.5.99 |

## Notes

- This plugin requires Python 3.12 or later
- Always test your plugin with the target NetBox version before upgrading in production
- Check the [NetBox release notes](https://docs.netbox.dev/en/stable/release-notes/) for breaking changes

## Upgrading

When upgrading NetBox or this plugin:

1. Review the NetBox release notes for any breaking changes
2. Test the upgrade in a development environment
3. Backup your database before upgrading production
4. Run database migrations: `python manage.py migrate`
5. Clear the cache: `python manage.py clearcache`
