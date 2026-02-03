"""
Test cases for {{ cookiecutter.project_name }} models.
"""

from django.core.exceptions import ValidationError

from ..models import {{ cookiecutter.__model_name }}
from ..testing import PluginModelTestCase
from ..testing.utils import create_tags, get_random_string


class {{ cookiecutter.__model_name }}TestCase(PluginModelTestCase):
    """Test {{ cookiecutter.__model_name }} model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        # Create test instances
        {{ cookiecutter.__model_name }}.objects.create(name='Test 1')
        {{ cookiecutter.__model_name }}.objects.create(name='Test 2')
        {{ cookiecutter.__model_name }}.objects.create(name='Test 3')

    def test_create_{{ cookiecutter.__model_url_name }}(self):
        """Test creating a {{ cookiecutter.__model_name }} instance."""
        name = f'Test {get_random_string(10)}'
        instance = {{ cookiecutter.__model_name }}.objects.create(name=name)

        self.assertEqual(instance.name, name)
        self.assertIsNotNone(instance.pk)

    def test_{{ cookiecutter.__model_url_name }}_str(self):
        """Test {{ cookiecutter.__model_name }} string representation."""
        instance = {{ cookiecutter.__model_name }}.objects.first()
        self.assertEqual(str(instance), instance.name)

    def test_{{ cookiecutter.__model_url_name }}_absolute_url(self):
        """Test {{ cookiecutter.__model_name }} get_absolute_url method."""
        instance = {{ cookiecutter.__model_name }}.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_{{ cookiecutter.__model_url_name }}_unique_name(self):
        """Test that {{ cookiecutter.__model_name }} names must be unique."""
        name = 'Duplicate Name'
        {{ cookiecutter.__model_name }}.objects.create(name=name)

        with self.assertRaises(ValidationError):
            instance = {{ cookiecutter.__model_name }}(name=name)
            instance.full_clean()

    def test_model_to_dict(self):
        """Test model_to_dict helper method."""
        instance = {{ cookiecutter.__model_name }}.objects.first()
        data = self.model_to_dict(instance)

        self.assertIn('name', data)
        self.assertEqual(data['name'], instance.name)
        self.assertIn('id', data)

    def test_instance_equal(self):
        """Test assertInstanceEqual helper method."""
        instance = {{ cookiecutter.__model_name }}.objects.first()

        # Should pass with matching data
        self.assertInstanceEqual(
            instance,
            {'name': instance.name, 'id': instance.pk}
        )

    def test_{{ cookiecutter.__model_url_name }}_with_tags(self):
        """Test {{ cookiecutter.__model_name }} with tags."""
        tags = create_tags(['important', 'test'])
        instance = {{ cookiecutter.__model_name }}.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_bulk_create(self):
        """Test bulk creation of {{ cookiecutter.__model_name }} instances."""
        initial_count = {{ cookiecutter.__model_name }}.objects.count()

        instances = [
            {{ cookiecutter.__model_name }}(name=f'Bulk {i}')
            for i in range(5)
        ]
        {{ cookiecutter.__model_name }}.objects.bulk_create(instances)

        self.assertEqual(
            {{ cookiecutter.__model_name }}.objects.count(),
            initial_count + 5
        )

    def test_query_filter(self):
        """Test filtering {{ cookiecutter.__model_name }} instances."""
        # Create a specific instance for filtering
        test_name = f'FilterTest {get_random_string(10)}'
        {{ cookiecutter.__model_name }}.objects.create(name=test_name)

        # Test filter
        results = {{ cookiecutter.__model_name }}.objects.filter(name=test_name)
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, test_name)

    def test_ordering(self):
        """Test {{ cookiecutter.__model_name }} default ordering."""
        instances = list({{ cookiecutter.__model_name }}.objects.all())

        # Check that instances are ordered by name
        names = [instance.name for instance in instances]
        self.assertEqual(names, sorted(names))


class {{ cookiecutter.__model_name }}ValidationTestCase(PluginModelTestCase):
    """Test {{ cookiecutter.__model_name }} validation."""

    def test_empty_name(self):
        """Test that empty name is not allowed."""
        with self.assertRaises(ValidationError):
            instance = {{ cookiecutter.__model_name }}(name='')
            instance.full_clean()

    def test_name_max_length(self):
        """Test name field max length."""
        long_name = 'x' * 101  # Exceeds max_length of 100

        with self.assertRaises(ValidationError):
            instance = {{ cookiecutter.__model_name }}(name=long_name)
            instance.full_clean()
