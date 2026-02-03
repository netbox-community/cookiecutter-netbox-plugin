"""
Test cases for {{ cookiecutter.project_name }} GraphQL API.
"""
{% if cookiecutter.include_graphql == "yes" -%}
from ..models import {{ cookiecutter.__model_name }}
from ..testing import PluginGraphQLTestCase


class {{ cookiecutter.__model_name }}GraphQLTestCase(PluginGraphQLTestCase):
    """Test {{ cookiecutter.__model_name }} GraphQL queries."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        {{ cookiecutter.__model_name }}.objects.create(name='GraphQL Test 1')
        {{ cookiecutter.__model_name }}.objects.create(name='GraphQL Test 2')
        {{ cookiecutter.__model_name }}.objects.create(name='GraphQL Test 3')

    def test_query_{{ cookiecutter.__model_url_name }}(self):
        """Test GraphQL query for a single {{ cookiecutter.__model_name }}."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        instance = {{ cookiecutter.__model_name }}.objects.first()

        query = (
            "query { "
            "{{ cookiecutter.__model_url_name }}(id: " + str(instance.pk) + ") { "
            "id name "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['{{ cookiecutter.__model_url_name }}']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)

    def test_query_{{ cookiecutter.__model_url_name }}_list(self):
        """Test GraphQL query for list of {{ cookiecutter.__model_name }}s."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        query = """
        query {
            {{ cookiecutter.__model_url_name }}_list {
                id
                name
            }
        }
        """

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['{{ cookiecutter.__model_url_name }}_list']
        self.assertEqual(len(data), 3)
        self.assertIn('id', data[0])
        self.assertIn('name', data[0])

    def test_query_{{ cookiecutter.__model_url_name }}_with_all_fields(self):
        """Test GraphQL query with all available fields."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        instance = {{ cookiecutter.__model_name }}.objects.first()

        query = (
            "query { "
            "{{ cookiecutter.__model_url_name }}(id: " + str(instance.pk) + ") { "
            "id name created last_updated "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['{{ cookiecutter.__model_url_name }}']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)
        self.assertIsNotNone(data['created'])
        self.assertIsNotNone(data['last_updated'])
{% else -%}
# GraphQL not enabled for this plugin
# To enable GraphQL support, regenerate the plugin with include_graphql=yes
{% endif %}
