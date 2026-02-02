# Tutorial

To start with, you will need [GitHub](https://github.com/), [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org/). If
you don't have one, please follow the links to apply one before you get started on this
tutorial.

If you are new to Git and GitHub, you should probably spend a few minutes on
some tutorials at the top of the page at [GitHub Help](https://help.github.com/).

You will also need an installation of [NetBox](https://github.com/netbox-community/netbox) to configure and test the plugin.
More information on Plugin Development can be found in the NetBox documentation
[Plugin Development](https://docs.netbox.dev/en/stable/plugins/development/).

## Step 1: Install Cookiecutter

Install cookiecutter:

``` bash
pip install cookiecutter
```

## Step 2: Generate Your Package

Now it's time to generate your Python package.

Run the following command and feed with answers. If you don't know what to enter, stick with the defaults:

```bash
cookiecutter https://github.com/netbox-community/cookiecutter-netbox-plugin.git
```

You'll be prompted for several options:
- **plugin_name**: The base name of your plugin (e.g., "HealthCheck")
- **include_rest_api**: Whether to include REST API support (yes/no)
- **include_graphql**: Whether to include GraphQL support (yes/no)
- **open_source_license**: Choose your preferred license

Finally, a new folder will be created under current folder, the name is the answer you
provided to `hyphenated`.

Go to this generated folder, the project layout should look like:

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

Go to your NetBox development environment and make sure the NetBox virtual environment is active. See [Create Python Virtual Environment](https://docs.netbox.dev/en/stable/development/getting-started/#4-create-a-python-virtual-environment).

To ease development, it is recommended to go ahead and install the plugin in editable mode (i.e setuptools' develop mode). Call pip from the plugin's root directory with the `-e` flag:

```no-highlight
$ pip install -e .
```

## Step 4: Configure NetBox

To enable the plugin in NetBox, add it to the `PLUGINS` parameter in `configuration.py`:

```python
PLUGINS = [
    'netbox_healthcheck_plugin',
]
```

At this point you can run tests and make sure everything is working properly.

## Step 5: Run Tests

The generated plugin includes comprehensive testing infrastructure. See the [Testing Guide](../TESTING.md) in your generated project for details.

To run tests locally (from your NetBox directory):

```bash
# Run all tests
python manage.py test netbox_healthcheck_plugin.tests --parallel -v2

# Run specific test file
python manage.py test netbox_healthcheck_plugin.tests.test_models
```

The CI workflow will automatically run tests on every push and pull request.

## Step 6: Create a GitHub Repo

Go to your GitHub account and create a new repo named `netbox-healthcheck-plugin`, where
`netbox-healthcheck-plugin` matches the `hyphenated` from your answers to running
cookiecutter.

!!! note "Trusted Publishing Recommended"
    Modern PyPI deployment uses [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) instead of API tokens. See [Step 9](#step-9-configuring-trusted-publishing) below for setup instructions.

## Step 7: Upload code to GitHub

Back to your develop environment, find the folder named after the `hyphenated`.
Move into this folder, and then setup git to use your GitHub repo and upload the
code:

``` bash
cd netbox-healthcheck-plugin

git add .
git commit -m "Initial commit."
git branch -M main
git remote add origin git@github.com:myusername/netbox-healthcheck-plugin.git
git push -u origin main
```

Where `myusername` and `netbox-healthcheck-plugin` are adjusted for your username and
repo name.

You'll need a ssh key to push the repo. You can [Generate](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) a key or
[Add](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) an existing one.

!!! warning "Pre-commit Hooks"
    If you answered 'yes' to install pre-commit hooks, they will run automatically on `git commit`.
    Some files may be modified by hooks. If so, please add these files and commit again.

### Check result

After pushing your code to GitHub, goto GitHub web page, navigate to your repo, then
click on actions link, you should find screen like this:

![](http://images.jieyu.ai/images/202104/20210419170304.png)

There should be some workflows running. The CI workflow tests your code automatically.

## Step 8: Check documentation

Documentation will be published and available at *https://{your_github_account}.github.io/{your_repo}*. You will
need to make sure GitHub is configured properly:

1. Your repo must be public
2. On the main top horizontal menu go to "Settings"
3. On the left-hand menu go to "Pages"
4. Under "Build and deployment" make sure Source dropdown is set to "Deploy from a branch"
5. Under branch choose "gh-pages" and "/(root)" - click the Save button

You may need to wait up to 10 minutes for your documentation to appear. If you are still having issues you
can manually deploy it by the following steps:

1. Make sure a local virtual environment is configured
2. Install documentation packages:

```bash
pip install mkdocs-material mkdocs-autorefs mkdocs-material-extensions mkdocstrings mkdocstrings-python-legacy mkdocs-include-markdown-plugin
```

3. Deploy documentation:

```bash
mkdocs gh-deploy
```

Documentation updates will be published once:

1. The commit is tagged, and the tag name starts with 'v' (lower case)
2. Build/testing executed by GitHub CI passed

## Step 9: Configuring trusted publishing

This guide uses PyPI's [trusted publishing](https://docs.pypi.org/trusted-publishers/) implementation to connect
to [GitHub Actions CI/CD](https://github.com/features/actions). This is recommended for security reasons, since
the generated tokens are created for each of your projects
individually and expire automatically.

!!! attention "Migration from API Tokens"

    If you followed earlier versions of this guide, you
    have created the secrets `PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN`
    for direct PyPI and TestPyPI access. These are obsolete now and
    you should remove them from your GitHub repository and revoke
    them in your PyPI and TestPyPI account settings in case you are replacing your old setup with the new one.

Since this guide will demonstrate uploading to both
PyPI and TestPyPI, we'll need two trusted publishers configured.
The following steps will lead you through creating the "pending" publishers
for your new PyPI project.
However it is also possible to add [trusted publishing](https://docs.pypi.org/trusted-publishers/) to any
pre-existing project, if you are its owner.

Let's begin! 🚀

1. Go to https://pypi.org/manage/account/publishing/
2. Fill in the name you wish to publish your new PyPI project under
   (the `name` value in your `pyproject.toml`),
   the GitHub repository owner's name (org or user),
   and repository name, and the name of the release workflow file under
   the `.github/` folder (use `publish-pypi.yaml`).
   Finally, add the name of the GitHub Environment
   (`pypi`) we'll set up under your repository.
   Register the trusted publisher.
3. Now, go to https://test.pypi.org/manage/account/publishing/ and repeat
   the second step, but this time, enter `testpypi` as the name of the
   GitHub Environment.
4. Your "pending" publishers are now ready for their first use and will
   create your projects automatically once you use them
   for the first time.

!!! note "TestPyPI Account"
    If you don't have a TestPyPI account, you'll need to
    create it. It's not the same as a regular PyPI account.

!!! warning "Manual Approval Required"
    For security reasons, you must require [manual approval](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-protection-rules)
    on each run for the `pypi` environment.

## Step 10: Make official release

After done with your phased development in a feature branch, make a pull request, following
instructions at [release checklist](pypi_release_checklist.md), trigger first official release and check
result at [PyPI](https://pypi.org).

## Step 11: (Optional) Submit to netbox.dev

If your plugin is public, submit it to [NetBox.dev Plugin Repository](https://netbox.dev/plugins/) for easy discovery by other NetBox users.

!!! tip "Questions or Feedback?"
    Did you find anything in this article confusing? Please **Edit this file** and create a pull request!
