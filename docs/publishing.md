# Publishing Your Plugin

Once your plugin is ready, you can publish it to share with the NetBox community.

## Prerequisites

You will need accounts on:
- [GitHub](https://github.com/) (already have this from the quickstart)
- [PyPI](https://pypi.org) - Python Package Index
- [TestPyPI](https://test.pypi.org/) - PyPI testing environment

## Documentation Setup

Your plugin documentation will be published at `https://{your_github_account}.github.io/{your_repo}`.

### GitHub Pages Configuration

Configure GitHub Pages for your repository:

1. Your repo must be public
2. Go to your repo's Settings
3. Navigate to Pages in the left menu
4. Under "Build and deployment":
   - Set Source to "Deploy from a branch"
   - Choose "gh-pages" branch and "/(root)" folder
   - Click Save

Documentation will appear within 10 minutes. If not, you can manually deploy:

1. Install documentation packages in your local environment:
   ```bash
   pip install mkdocs-material mkdocs-autorefs mkdocs-material-extensions mkdocstrings mkdocstrings-python-legacy mkdocs-include-markdown-plugin
   ```

2. Deploy:
   ```bash
   mkdocs gh-deploy
   ```

!!! note "Automatic Updates"
    Documentation updates are published automatically when:

    1. A commit is tagged with a version starting with 'v' (e.g., v1.0.0)
    2. GitHub CI tests pass

## Configuring Trusted Publishing

Modern PyPI deployment uses [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) instead of API tokens. This is more secure because tokens are created per-project and expire automatically.

!!! attention "Migrating from API Tokens"
    If you previously used API tokens (`PYPI_API_TOKEN` and `TEST_PYPI_API_TOKEN` secrets), remove them from your GitHub repository and revoke them in PyPI/TestPyPI account settings.

### Set Up Trusted Publishers

Since we'll publish to both PyPI and TestPyPI, you need two trusted publishers configured.

#### PyPI Setup

1. Go to https://pypi.org/manage/account/publishing/
2. Fill in the form:
   - **PyPI Project Name**: The `name` value from your `pyproject.toml`
   - **Owner**: Your GitHub username or organization
   - **Repository name**: Your repository name (e.g., `netbox-healthcheck-plugin`)
   - **Workflow name**: `publish-pypi.yaml`
   - **Environment name**: `pypi`
3. Click "Add" to register the trusted publisher

#### TestPyPI Setup

1. Go to https://test.pypi.org/manage/account/publishing/
2. Fill in the same form as above, but use:
   - **Environment name**: `testpypi`
3. Click "Add" to register the trusted publisher

!!! note "TestPyPI Account"
    TestPyPI requires a separate account from PyPI. Create one at https://test.pypi.org if needed.

!!! warning "Manual Approval Required"
    For security, configure [manual approval](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#deployment-protection-rules) for the `pypi` environment in your GitHub repository settings.

Your "pending" publishers are now ready. They'll automatically create your PyPI projects on first use.

## Making Your First Release

When you're ready to release:

1. **Update version number** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create a pull request** with your changes
4. **Merge to main branch** after review and tests pass
5. **Create a git tag** and push:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

The GitHub Actions workflow will automatically:
- Run tests
- Build the package
- Publish to PyPI (after manual approval)
- Deploy documentation
- Create a GitHub release with changelog

See the [Release Checklist](pypi_release_checklist.md) for detailed step-by-step instructions.

## Submit to NetBox.dev

Share your plugin with the community by submitting it to the [NetBox Plugin Registry](https://netbox.dev/plugins/).

Benefits:
- Increased visibility
- Easier discovery by NetBox users
- Listed in the official plugin directory

To submit:
1. Go to https://netbox.dev/plugins/
2. Click "Submit a Plugin"
3. Follow the submission instructions

## Best Practices

- **Semantic Versioning**: Use [semver](https://semver.org/) for version numbers (MAJOR.MINOR.PATCH)
- **Keep Changelog Updated**: Document all changes between releases
- **Test Before Release**: Ensure all tests pass and documentation builds
- **Tag Releases**: Use git tags that match version numbers (v1.0.0, v1.0.1, etc.)
- **Write Good Release Notes**: Help users understand what changed

## Troubleshooting

### Documentation Not Building

Check the Actions tab in your GitHub repository for error messages. Common issues:
- Missing dependencies in mkdocs.yml
- Broken markdown syntax
- Invalid links

### Publishing Fails

- Verify trusted publishing is configured correctly in PyPI/TestPyPI
- Check that environment names match in both PyPI and GitHub workflow
- Ensure version number in pyproject.toml hasn't been used before

## Getting Help

- **[PyPI Help](https://pypi.org/help/)** - PyPI documentation
- **[GitHub Actions Docs](https://docs.github.com/en/actions)** - Workflow help
- **[NetBox Discussions](https://github.com/netbox-community/netbox/discussions)** - Community support
