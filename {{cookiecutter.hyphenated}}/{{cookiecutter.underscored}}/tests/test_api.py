"""
Test cases for {{ cookiecutter.project_name }} REST API.
"""
{% if cookiecutter.include_rest_api == "yes" -%}
from django.urls import reverse

from ..models import {{ cookiecutter.__model_name }}
from ..testing import PluginAPITestCase
from ..testing.utils import get_random_string, disable_warnings


class {{ cookiecutter.__model_name }}APITestCase(PluginAPITestCase):
    """Test {{ cookiecutter.__model_name }} API endpoints."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        {{ cookiecutter.__model_name }}.objects.create(name='API Test 1')
        {{ cookiecutter.__model_name }}.objects.create(name='API Test 2')
        {{ cookiecutter.__model_name }}.objects.create(name='API Test 3')

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.list_url_name = 'plugins-api:{{ cookiecutter.underscored }}-api:{{ cookiecutter.__model_url_name }}-list'
        self.detail_url_name = 'plugins-api:{{ cookiecutter.underscored }}-api:{{ cookiecutter.__model_url_name }}-detail'

    def test_list_{{ cookiecutter.__model_url_name }}s(self):
        """Test GET request to list {{ cookiecutter.__model_name }}s."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        url = self._get_list_url()
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertIn('results', response.data)

    def test_list_{{ cookiecutter.__model_url_name }}s_without_permission(self):
        """Test GET request without permission."""
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_get_{{ cookiecutter.__model_url_name }}(self):
        """Test GET request for a single {{ cookiecutter.__model_name }}."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = self._get_detail_url(instance)
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['id'], instance.pk)
        self.assertEqual(response.data['name'], instance.name)

    def test_create_{{ cookiecutter.__model_url_name }}(self):
        """Test POST request to create a {{ cookiecutter.__model_name }}."""
        self.add_permissions('{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}')

        url = self._get_list_url()
        name = f'API Created {get_random_string(10)}'

        data = {
            'name': name,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)

        # Verify object was created
        instance = {{ cookiecutter.__model_name }}.objects.get(name=name)
        self.assertEqual(instance.name, name)
        self.assertEqual(response.data['id'], instance.pk)

    def test_create_{{ cookiecutter.__model_url_name }}_without_permission(self):
        """Test POST request without permission."""
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.post(url, {'name': 'Test'}, format='json')
            self.assertHttpStatus(response, 403)

    def test_bulk_create_{{ cookiecutter.__model_url_name }}s(self):
        """Test bulk creation via API."""
        self.add_permissions('{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}')

        url = self._get_list_url()
        data = [
            {'name': f'Bulk {i}'} for i in range(1, 4)
        ]

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)
        self.assertEqual(len(response.data), 3)

        # Verify objects were created
        for item in data:
            self.assertTrue(
                {{ cookiecutter.__model_name }}.objects.filter(name=item['name']).exists()
            )

    def test_update_{{ cookiecutter.__model_url_name }}(self):
        """Test PATCH request to update a {{ cookiecutter.__model_name }}."""
        self.add_permissions('{{ cookiecutter.underscored }}.change_{{ cookiecutter.__model_url_name }}')

        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = self._get_detail_url(instance)
        new_name = f'Updated {get_random_string(10)}'

        data = {'name': new_name}

        response = self.client.patch(url, data, format='json')
        self.assertHttpStatus(response, 200)

        # Verify object was updated
        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_update_{{ cookiecutter.__model_url_name }}_without_permission(self):
        """Test PATCH request without permission."""
        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = self._get_detail_url(instance)

        with disable_warnings('django.request'):
            response = self.client.patch(url, {'name': 'Test'}, format='json')
            self.assertHttpStatus(response, 403)

    def test_delete_{{ cookiecutter.__model_url_name }}(self):
        """Test DELETE request to remove a {{ cookiecutter.__model_name }}."""
        self.add_permissions('{{ cookiecutter.underscored }}.delete_{{ cookiecutter.__model_url_name }}')

        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = self._get_detail_url(instance)

        response = self.client.delete(url)
        self.assertHttpStatus(response, 204)

        # Verify object was deleted
        self.assertFalse(
            {{ cookiecutter.__model_name }}.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_{{ cookiecutter.__model_url_name }}_without_permission(self):
        """Test DELETE request without permission."""
        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = self._get_detail_url(instance)

        with disable_warnings('django.request'):
            response = self.client.delete(url)
            self.assertHttpStatus(response, 403)

    def test_options_{{ cookiecutter.__model_url_name }}(self):
        """Test OPTIONS request for API metadata."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        url = self._get_list_url()
        response = self.client.options(url)

        self.assertHttpStatus(response, 200)
        self.assertIn('actions', response.data)


class {{ cookiecutter.__model_name }}APIValidationTestCase(PluginAPITestCase):
    """Test {{ cookiecutter.__model_name }} API validation."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions('{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}')
        self.list_url_name = 'plugins-api:{{ cookiecutter.underscored }}-api:{{ cookiecutter.__model_url_name }}-list'

    def test_create_with_empty_name(self):
        """Test that API validates empty name."""
        url = self._get_list_url()
        data = {'name': ''}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('name', response.data)

    def test_create_with_duplicate_name(self):
        """Test that API validates duplicate names."""
        existing = {{ cookiecutter.__model_name }}.objects.create(name='Duplicate')

        url = self._get_list_url()
        data = {'name': 'Duplicate'}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)

    def test_create_with_missing_required_field(self):
        """Test that API validates required fields."""
        url = self._get_list_url()
        data = {}  # Missing name

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('name', response.data)
{% else -%}
# REST API not enabled for this plugin
# To enable API support, regenerate the plugin with include_rest_api=yes
{% endif %}
