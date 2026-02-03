# Quickstart

This guide will help you create and test a NetBox plugin in minutes.

## Prerequisites

You will need:
- [NetBox](https://github.com/netbox-community/netbox) development environment
- Python 3.11 or higher
- Git and [GitHub](https://github.com/) account

If you are new to Git and GitHub, check out the tutorials at [GitHub Help](https://help.github.com/).

For more information on Plugin Development, see the NetBox documentation on [Plugin Development](https://netboxlabs.com/docs/netbox/plugins/development/).

## Step 1: Install Cookiecutter

Install cookiecutter:

``` bash
pip install cookiecutter
```

## Step 2: Generate Your Package

Run the following command and provide your answers:

```bash
cookiecutter https://github.com/netbox-community/cookiecutter-netbox-plugin.git
```

You'll be prompted for several options:
- **plugin_name**: The base name of your plugin (e.g., "HealthCheck")
- **include_rest_api**: Whether to include REST API support (yes/no)
- **include_graphql**: Whether to include GraphQL support (yes/no)
- **open_source_license**: Choose your preferred license

A new folder will be created with the name matching your `hyphenated` answer.

Go to this generated folder. The project layout should look like:

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yaml
│   │   ├── feature_request.yaml
│   │   └── housekeeping.yaml
│   └── workflows/
│       ├── ci.yaml              # Automated testing
│       ├── mkdocs.yaml          # Documentation deployment
│       └── publish-pypi.yaml    # Package publishing
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── COMPATIBILITY.md
├── CONTRIBUTING.md
├── docs/
│   ├── changelog.md
│   ├── contributing.md
│   └── index.md
├── LICENSE
├── Makefile
├── MANIFEST.in
├── mkdocs.yml
├── netbox_healthcheck_plugin/
│   ├── api/                     # REST API (optional)
│   │   ├── __init__.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── migrations/              # Database migrations
│   │   └── __init__.py
│   ├── templates/
│   │   └── netbox_healthcheck_plugin/
│   │       └── healthcheck.html
│   ├── testing/                 # Base test classes
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_models.py
│   │   └── test_views.py
│   ├── __init__.py
│   ├── filtersets.py
│   ├── forms.py
│   ├── graphql.py               # GraphQL (optional)
│   ├── models.py
│   ├── navigation.py
│   ├── search.py                # Global search integration
│   ├── tables.py
│   ├── urls.py
│   └── views.py
├── testing/
│   └── configuration.py         # NetBox test configuration
├── pyproject.toml
├── README.md
├── requirements_dev.txt
└── TESTING.md                   # Testing guide

```

Here the plugin_name is `HealthCheck`. When you generate yours, it may have a different name.

!!! note "Optional Components"
    - The `api/` directory is only created if you select `include_rest_api = yes`
    - The `graphql.py` file is only created if you select `include_graphql = yes`

### Key Features Included

The generated plugin includes several pre-configured features:

- **Models** (`models.py`) - NetBox model with tags and custom fields support
- **Views** (`views.py`) - CRUD views for web UI
- **Forms** (`forms.py`) - Model forms for data entry
- **Tables** (`tables.py`) - Data tables for list views
- **Navigation** (`navigation.py`) - Menu integration
- **Filtersets** (`filtersets.py`) - Search and filter functionality
- **Search** (`search.py`) - Global search integration
- **Testing** (`testing/`, `tests/`) - Comprehensive test infrastructure
- **API** (`api/`) - REST API endpoints (optional)
- **GraphQL** (`graphql.py`) - GraphQL schema (optional)

## Step 3: Development Installation

Go to your NetBox development environment and make sure the NetBox virtual environment is active. See [Create Python Virtual Environment](https://netboxlabs.com/docs/netbox/development/getting-started/#create-a-python-virtual-environment).

To ease development, install the plugin in editable mode. From the plugin's root directory:

```bash
pip install -e .
```

## Step 4: Configure NetBox

Enable the plugin in NetBox by adding it to the `PLUGINS` parameter in `configuration.py`:

```python
PLUGINS = [
    'netbox_healthcheck_plugin',
]
```

## Step 5: Create Database Migrations

Your plugin includes a model that needs a database table.

Make sure your NetBox virtual environment is active. See [Create a Virtual Environment](https://netboxlabs.com/docs/netbox/plugins/development/#create-a-virtual-environment) in the NetBox plugin development guide.

Then create and run migrations for your plugin. For detailed instructions, see [Database Migrations](https://netboxlabs.com/docs/netbox/plugins/development/models/#database-migrations) in the NetBox documentation.

!!! tip "Migration Management"
    Whenever you modify your plugin's models (add fields, change field types, etc.), you'll need to create new migrations. Always commit migration files to your repository.

## Step 6: Run Tests

The generated plugin includes comprehensive testing infrastructure. See the [Testing Guide](../TESTING.md) in your generated project for details.

To run tests locally (from your NetBox directory):

```bash
# Run all tests
$ ./manage.py test netbox_healthcheck_plugin.tests --parallel -v2

# Run specific test file
$ ./manage.py test netbox_healthcheck_plugin.tests.test_models
```

The CI workflow will automatically run tests on every push and pull request.

## Step 7: Create a GitHub Repo

Go to your GitHub account and create a new repo named `netbox-healthcheck-plugin`, matching the `hyphenated` name from your cookiecutter answers.

## Step 8: Upload Code to GitHub

From your plugin folder, initialize git and push to GitHub:

``` bash
cd netbox-healthcheck-plugin

git add .
git commit -m "Initial commit."
git branch -M main
git remote add origin git@github.com:myusername/netbox-healthcheck-plugin.git
git push -u origin main
```

Replace `myusername` and `netbox-healthcheck-plugin` with your username and repo name.

You'll need an ssh key to push the repo. You can [Generate](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) a key or [Add](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) an existing one.

!!! warning "Pre-commit Hooks"
    Pre-commit hooks will run automatically on `git commit`. Some files may be modified by hooks. If so, add these files and commit again.

### Check Result

After pushing your code to GitHub, navigate to your repo and click the Actions tab. You should see the CI workflow running automatically to test your code.

## Next Steps

Now that your plugin is working:

- **[Extend Your Plugin](extending.md)** - Add features and customize your plugin
- **[Publish Your Plugin](publishing.md)** - Share your plugin with the community

!!! tip "Questions or Feedback?"
    Find something confusing? Please **Edit this file** and create a pull request!
