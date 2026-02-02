# Prompts

When you create a package, you are prompted to enter these values.

## Templated Values

The following appear in various parts of your generated project.


## Templated Values

The following appear in various parts of your generated project.

<dl>
<dt>plugin_name</dt>
<dd>The base name of your plugin (without "NetBox" or "Plugin").  This is used
to initialize most of the other settings.</dd>

<dt>project_name</dt>
<dd>The name of your new Python package project. This is used in
documentation, so spaces and any characters are fine here.</dd>

<dt>hyphenated</dt>
<dd>The name of your Python package for PyPI, also as the repository name of GitHub.
Typically, it is the slugified version of project_name.</dd>

<dt>underscored</dt>
<dd>The name of the python module and directory in the project.</dd>

<dt>project_short_description</dt>
<dd>A 1-sentence description of what your Python package does.</dd>

<dt>full_name</dt>
<dd>Your full name.</dd>

<dt>email</dt>
<dd>Your email address.</dd>

<dt>github_username</dt>
<dd>Your GitHub username (or organization name).</dd>

<dt>version</dt>
<dd>The starting version number of the package.</dd>
</dl>

## Options

The following package configuration options set up different features
for your project.

<dl>
<dt>open_source_license</dt>
<dd>Choose a license. Options: [1. Apache-2.0, 2. MIT, 3. BSD, 4. ISC, 5. GPL-3.0-only, 6. Not open source]</dd>

<dt>include_rest_api</dt>
<dd>Include REST API support for your plugin. Options: [1. yes, 2. no]<br>
When enabled, generates a complete REST API structure with:
<ul>
<li>Serializers for NetBox model serialization</li>
<li>ViewSets for API endpoints</li>
<li>URL routing configuration</li>
<li>Integration with NetBox's REST API framework</li>
</ul>
This follows NetBox best practices for plugin API development and provides automatic CRUD operations for your models through the REST API.
</dd>

<dt>include_graphql</dt>
<dd>Include GraphQL support for your plugin. Options: [1. yes, 2. no]<br>
When enabled, generates GraphQL schema and resolvers:
<ul>
<li>GraphQL type definitions for your models</li>
<li>Query resolvers for data fetching</li>
<li>Integration with NetBox's GraphQL API</li>
</ul>
This allows your plugin's data to be queried through NetBox's GraphQL endpoint, providing flexible and efficient data retrieval.
</dd>
</dl>

except above settings, for CI/CD, you'll also need configure gitub repsitory secrets
at page repo > settings > secrtes, and add the following secrets:

- PERSONAL_TOKEN (required for publishing document to git pages)
- TEST_PYPI_API_TOKEN (required for publishing dev release to testpypi)
- PYPI_API_TOKEN (required for publish )
