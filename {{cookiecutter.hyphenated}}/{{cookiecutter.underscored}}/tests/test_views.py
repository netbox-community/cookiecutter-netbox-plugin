"""
Test cases for {{ cookiecutter.project_name }} views.
"""

from django.urls import reverse

from ..models import {{ cookiecutter.__model_name }}
from ..testing import PluginViewTestCase
from ..testing.utils import disable_warnings, get_random_string


class {{ cookiecutter.__model_name }}ViewTestCase(PluginViewTestCase):
    """Test {{ cookiecutter.__model_name }} views."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        {{ cookiecutter.__model_name }}.objects.create(name='View Test 1')
        {{ cookiecutter.__model_name }}.objects.create(name='View Test 2')
        {{ cookiecutter.__model_name }}.objects.create(name='View Test 3')

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.base_url = 'plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}'

    def test_list_{{ cookiecutter.__model_url_name }}s(self):
        """Test {{ cookiecutter.__model_name }} list view."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_{{ cookiecutter.__model_url_name }}s_without_permission(self):
        """Test {{ cookiecutter.__model_name }} list view without permission."""
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_{{ cookiecutter.__model_url_name }}(self):
        """Test {{ cookiecutter.__model_name }} detail view."""
        self.add_permissions('{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}')

        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_{{ cookiecutter.__model_url_name }}(self):
        """Test creating a {{ cookiecutter.__model_name }} via form."""
        self.add_permissions(
            '{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}',
            '{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}'
        )

        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_add')
        name = f'Created {get_random_string(10)}'

        form_data = self.post_data({
            'name': name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was created
        instance = {{ cookiecutter.__model_name }}.objects.get(name=name)
        self.assertEqual(instance.name, name)

    def test_create_{{ cookiecutter.__model_url_name }}_without_permission(self):
        """Test creating a {{ cookiecutter.__model_name }} without permission."""
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_{{ cookiecutter.__model_url_name }}(self):
        """Test editing a {{ cookiecutter.__model_name }} via form."""
        self.add_permissions(
            '{{ cookiecutter.underscored }}.change_{{ cookiecutter.__model_url_name }}',
            '{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}'
        )

        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_edit', kwargs={'pk': instance.pk})

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data({
            'name': new_name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was updated
        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_delete_{{ cookiecutter.__model_url_name }}(self):
        """Test deleting a {{ cookiecutter.__model_name }}."""
        self.add_permissions(
            '{{ cookiecutter.underscored }}.delete_{{ cookiecutter.__model_url_name }}',
            '{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}'
        )

        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_delete', kwargs={'pk': instance.pk})

        # Confirm deletion
        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was deleted
        self.assertFalse(
            {{ cookiecutter.__model_name }}.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_{{ cookiecutter.__model_url_name }}_without_permission(self):
        """Test deleting a {{ cookiecutter.__model_name }} without permission."""
        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class {{ cookiecutter.__model_name }}FormTestCase(PluginViewTestCase):
    """Test {{ cookiecutter.__model_name }} form validation."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions(
            '{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}',
            '{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}'
        )

    def test_form_validation_empty_name(self):
        """Test form validation with empty name."""
        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_add')
        form_data = self.post_data({'name': ''})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should not create object
        self.assertEqual({{ cookiecutter.__model_name }}.objects.filter(name='').count(), 0)

    def test_form_validation_duplicate_name(self):
        """Test form validation with duplicate name."""
        {{ cookiecutter.__model_name }}.objects.create(name='Duplicate')

        url = reverse('plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}_add')
        form_data = self.post_data({'name': 'Duplicate'})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should only have one instance with this name
        self.assertEqual({{ cookiecutter.__model_name }}.objects.filter(name='Duplicate').count(), 1)
