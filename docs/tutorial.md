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

Run the following command and feed with answers, If you don’t know what to enter, stick with the defaults:

```bash
cookiecutter https://github.com/netbox-community/cookiecutter-netbox-plugin.git
```

Finally, a new folder will be created under current folder, the name is the answer you
provided to `hyphenated`.

Go to this generated folder, the project layout should look like:

```
.
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docs
│   ├── changelog.md
│   ├── contributing.md
│   └── index.md
├── LICENSE
├── Makefile
├── MANIFEST.in
├── mkdocs.yml
├── netbox_healthcheck_plugin
│   ├── filtersets.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── navigation.py
│   ├── tables.py
│   ├── templates
│   │   └── netbox_healthcheck_plugin
│   │       └── healthcheck.html
│   ├── urls.py
│   └── views.py
├── pyproject.toml
├── README.md
├── requirements_dev.txt
└── tests
    ├── __init__.py
    └── test_netbox_healthcheck_plugin.py

```

Here the plugin_name is `HealthCheck`, when you generate yours, it could be other name.

## Step 3: Development Installation

Go to your NetBox development environment and make sure the NetBox virtual environment is active.  See [Create Python Virtual Environment](https://docs.netbox.dev/en/stable/development/getting-started/#4-create-a-python-virtual-environment).

To ease development, it is recommended to go ahead and install the plugin in editable mode (i.e setuptools' develop mode). Call pip from the plugin's root directory with the `-e` flag:

```no-highlight
$ pip install -e .
```

## Step 4: Configure NetBox

To enable the plugin in NetBox, add it to the `PLUGINS` parameter in `configuration.py`:

```python
PLUGINS = [
    'healthcheck',
]
```
At this point you can run tests and make sure everything is working properly.

## Step 5: Create a GitHub Repo

Go to your GitHub account and create a new repo named `netbox-healthcheck-plugin`, where
`netbox-healthcheck-plugin` matches the `hyphenated` from your answers to running
cookiecutter.

Then go to repo > settings > secrets, click on 'New repository secret', add the following
 secrets:

- TEST_PYPI_API_TOKEN, see [How to apply TestPyPI token](https://test.pypi.org/manage/account/)
- PYPI_API_TOKEN, see [How to apply pypi token](https://pypi.org/manage/account/)
- PERSONAL_TOKEN, see [How to apply personal token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

## Step 6: Upload code to GitHub

Back to your develop environment, find the folder named after the `hyphenated`.
Move into this folder, and then setup git to use your GitHub repo and upload the
code:

``` bash
cd my-package

git add .
git commit -m "Initial commit."
git branch -M main
git remote add origin git@github.com:myusername/my-package.git
git push -u origin main
```

Where `myusername` and `my-package` are adjusted for your username and
repo name.

You'll need a ssh key to push the repo. You can [Generate](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) a key or
[Add](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/) an existing one.

???+ Warning

    if you answered 'yes' to the question if install pre-commit hooks at last step,
    then you should find pre-commit be invoked when you run `git commit`, and some files
     may be modified by hooks. If so, please add these files and **commit again**.

### Check result

After pushing your code to GitHub, goto GitHub web page, navigate to your repo, then
click on actions link, you should find screen like this:

![](http://images.jieyu.ai/images/202104/20210419170304.png)

There should be some workflows running. After they finished, go to [TestPyPI], check if a
new artifact is published under the name `hyphenated`.

## Step 7. Check documentation

Documentation will be published and available at *https://{your_github_account}.github.io/{your_repo}* You will
need to make sure GitHub is configured properly:

1. Your repro must be public
2. On the main top horizontal menu go to "Settings"
2. On the left-hand menu go to "Pages"
3. Under "Build and deployment" make sure Source dropdown is set to "Deploy from a branch"
4. Under branch choose "gh-pages" and "/(root)" - click the Save button

You may need to wait up to 10 minutes for your documentation to appear.  If you are still having issues you
can manually deploy it by the following steps:

1. Make sure a local virtual environment is configured.
2. Pip install the following pakcages:

```
pip install mkdocs-material mkdocs-autorefs mkdocs-material-extensions mkdocstrings mkdocstrings-python-legacy mkdocs-include-markdown-plugin
```
3. run the following command:

```
mkdocs gh-deploy
```

Documentation updates will be published once:

1. the commit is tagged, and the tag name is started with 'v' (lower case)
2. build/testing executed by GitHub CI passed

## Step 8. Make official release

  After done with your phased development in a feature branch, make a pull request, following
  instructions at [release checklist](pypi_release_checklist.md), trigger first official release and check
  result at [PyPI].

### Configuring trusted publishing

This guide relies on PyPI's [trusted publishing](https://docs.pypi.org/trusted-publishers/) implementation to connect
to [GitHub Actions CI/CD](https://github.com/features/actions). This is recommended for security reasons, since
the generated tokens are created for each of your projects
individually and expire automatically. Otherwise, you'll need to generate an
[API token](https://pypi.org/help/#apitoken) for both PyPI and TestPyPI. In case of publishing to third-party
indexes like `devpi <devpi:index>`, you may need to provide a
username/password combination.

Since this guide will demonstrate uploading to both
PyPI and TestPyPI, we'll need two trusted publishers configured.
The following steps will lead you through creating the "pending" publishers
for your new :term:`PyPI project <Project>`.
However it is also possible to add [trusted publishing](https://docs.pypi.org/trusted-publishers/) to any
pre-existing project, if you are its owner.

.. attention::

   If you followed earlier versions of this guide, you
   have created the secrets `PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN`
   for direct PyPI and TestPyPI access. These are obsolete now and
   you should remove them from your GitHub repository and revoke
   them in your PyPI and TestPyPI account settings in case you are replacing your old setup with the new one.


Let's begin! 🚀

1. Go to https://pypi.org/manage/account/publishing/.
2. Fill in the name you wish to publish your new
   `PyPI project <Project>` under
   (the `name` value in your `setup.cfg` or `pyproject.toml`),
   the GitHub repository owner's name (org or user),
   and repository name, and the name of the release workflow file under
   the `.github/` folder, see `workflow-definition`.
   Finally, add the name of the GitHub Environment
   (`pypi`) we're going set up under your repository.
   Register the trusted publisher.
3. Now, go to https://test.pypi.org/manage/account/publishing/ and repeat
   the second step, but this time, enter `testpypi` as the name of the
   GitHub Environment.
4. Your "pending" publishers are now ready for their first use and will
   create your projects automatically once you use them
   for the first time.

!!! note

    If you don't have a TestPyPI account, you'll need to
    create it. It's not the same as a regular PyPI account.


!!! warning

    For security reasons, you must require `manual approval <https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-protection-rules>`_
    on each run for the ``pypi`` environment.

## Step 9. (Optional) Submit it to netbox.dev

If your plugin is public, submit it to [NetBox.dev Plugin Repository](https://netbox.dev/plugins/) for easy discovery by other NetBox users.

??? Note
    Did you find anything in this article confusing? Please **Edit this file** and create a pull a request!
