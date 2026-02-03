"""
Standalone testing base classes for {{ cookiecutter.project_name }}.

These classes provide common testing patterns.
"""

from contextlib import contextmanager
from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from django.test import Client
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.constants import TOKEN_PREFIX
from users.models import ObjectPermission, Token
from utilities.permissions import resolve_permission_type

User = get_user_model()


class PluginTestCase(DjangoTestCase):
    """
    Base test case for plugin tests with common setup and utilities.

    Provides:
    - Test user creation with configurable permissions
    - Permission management helpers
    - Enhanced HTTP status assertions
    - Transaction-based subtests with automatic cleanup
    """

    user_permissions: list[str] = []

    def setUp(self):
        """Create a test user with optional permissions."""
        self.user = self.create_test_user()
        self.client = Client()
        self.client.force_login(self.user)

        # Add permissions if specified
        if self.user_permissions:
            self.add_permissions(*self.user_permissions)

    def create_test_user(self, username: str = "testuser",
                        is_superuser: bool = False) -> User:
        """
        Create a test user with sensible defaults.

        Args:
            username: Username for the test user
            is_superuser: Whether user is a superuser

        Returns:
            User instance
        """
        return User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            is_superuser=is_superuser,
            password="testpass123"
        )

    def add_permissions(self, *permissions: str):
        """
        Assign permissions to the test user using NetBox's ObjectPermission system.

        Args:
            *permissions: Permission names in format "app.action_model"
                         e.g., "{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}"

        Example:
            self.add_permissions(
                "{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}",
                "{{ cookiecutter.underscored }}.add_{{ cookiecutter.__model_url_name }}",
            )
        """
        for name in permissions:
            object_type, action = resolve_permission_type(name)
            obj_perm = ObjectPermission(name=name, actions=[action])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(object_type)

    def remove_permissions(self, *permissions: str):
        """
        Remove permissions from the test user.

        Args:
            *permissions: Permission names in format "app.action_model"
        """
        for name in permissions:
            object_type, action = resolve_permission_type(name)
            ObjectPermission.objects.filter(
                actions__contains=[action],
                object_types=object_type,
                users=self.user
            ).delete()

    def assertHttpStatus(self, response, expected_status: int, msg: str = None):
        """
        Enhanced HTTP status assertion with detailed error information.

        Args:
            response: Django response object
            expected_status: Expected HTTP status code
            msg: Optional custom message
        """
        if response.status_code != expected_status:
            error_msg = (
                f"Expected HTTP {expected_status}, got {response.status_code}"
            )

            # Add response content if available
            if hasattr(response, 'data'):
                error_msg += f"\nResponse data: {response.data}"
            elif hasattr(response, 'content'):
                content = response.content.decode('utf-8')[:500]
                error_msg += f"\nResponse content: {content}"

            if msg:
                error_msg = f"{msg}\n{error_msg}"

            self.fail(error_msg)

    @contextmanager
    def cleanupSubTest(self, **params):
        """
        Context manager for running subtests with automatic database cleanup.

        Uses Django's transaction savepoints to rollback changes after each
        subtest, allowing multiple test scenarios without data pollution.

        Example:
            for scenario in ['with_tags', 'without_tags']:
                with self.cleanupSubTest(scenario=scenario):
                    # Test code here - DB changes will be rolled back
                    pass
        """
        sid = transaction.savepoint()
        try:
            with self.subTest(**params):
                yield
        finally:
            transaction.savepoint_rollback(sid)


class PluginModelTestCase(PluginTestCase):
    """
    Base test case for model testing with instance comparison utilities.

    Provides:
    - Model instance comparison
    - Field-by-field comparison with exclusions
    - Support for foreign keys and many-to-many relationships
    """

    def assertInstanceEqual(self, instance, data: dict[str, Any],
                          exclude: set[str | None] = None,
                          api: bool = False):
        """
        Compare a model instance against a dictionary of expected values.

        Handles:
        - Foreign key relationships (compares PKs)
        - Many-to-many relationships (compares sorted PKs)
        - Regular fields (direct comparison)

        Args:
            instance: Model instance to compare
            data: Dictionary of expected field values
            exclude: Set of field names to exclude from comparison
            api: If True, use API representation format

        Example:
            self.assertInstanceEqual(
                obj,
                {'name': 'Test', 'tags': [tag1.pk, tag2.pk]},
                exclude={'created', 'last_updated'}
            )
        """
        exclude = exclude or set()
        model_dict = self.model_to_dict(instance, exclude=exclude, api=api)

        for field_name, expected_value in data.items():
            if field_name in exclude:
                continue

            actual_value = model_dict.get(field_name)
            self.assertEqual(
                actual_value,
                expected_value,
                f"Field '{field_name}' mismatch: {actual_value} != {expected_value}"
            )

    def model_to_dict(self, instance, exclude: set[str | None] = None,
                     api: bool = False) -> dict[str, Any]:
        """
        Convert a model instance to a dictionary for comparison.

        Args:
            instance: Model instance to convert
            exclude: Fields to exclude
            api: If True, use API representation format

        Returns:
            Dictionary of field names to values
        """
        exclude = exclude or set()
        data = {}

        for field in instance._meta.get_fields():
            if field.name in exclude:
                continue

            # Skip reverse relations
            if field.one_to_many or field.one_to_one:
                continue

            # Handle many-to-many
            if field.many_to_many:
                value = [obj.pk for obj in getattr(instance, field.name).all()]
                data[field.name] = sorted(value)

            # Handle foreign key
            elif field.many_to_one:
                related_obj = getattr(instance, field.name)
                data[field.name] = related_obj.pk if related_obj else None

            # Handle regular field
            else:
                data[field.name] = getattr(instance, field.name)

        return data


class PluginAPITestCase(PluginModelTestCase):
    """
    Base test case for REST API endpoint testing.

    Provides:
    - APIClient with token authentication
    - URL generation helpers
    - Common API test patterns
    """

    def setUp(self):
        """Set up API client with token authentication."""
        super().setUp()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {TOKEN_PREFIX}{self.token.key}.{self.token.token}')

    def _get_list_url(self) -> str:
        """
        Get the list URL for the model being tested.

        Override this method or set self.list_url_name in your test class.

        Returns:
            URL string for the list endpoint
        """
        if hasattr(self, 'list_url_name'):
            return reverse(self.list_url_name)
        raise NotImplementedError("Set self.list_url_name or override _get_list_url()")

    def _get_detail_url(self, instance) -> str:
        """
        Get the detail URL for a specific instance.

        Override this method or set self.detail_url_name in your test class.

        Args:
            instance: Model instance

        Returns:
            URL string for the detail endpoint
        """
        if hasattr(self, 'detail_url_name'):
            return reverse(self.detail_url_name, kwargs={'pk': instance.pk})
        raise NotImplementedError("Set self.detail_url_name or override _get_detail_url()")

    def assertHttpStatus(self, response, expected_status: int, msg: str = None):
        """Enhanced HTTP status for API responses with JSON data."""
        if response.status_code != expected_status:
            error_msg = (
                f"Expected HTTP {expected_status}, got {response.status_code}"
            )

            # Add JSON response data
            if hasattr(response, 'data'):
                error_msg += f"\nResponse data: {response.data}"

            if msg:
                error_msg = f"{msg}\n{error_msg}"

            self.fail(error_msg)


class PluginViewTestCase(PluginModelTestCase):
    """
    Base test case for web view testing.

    Provides:
    - URL generation helpers
    - Form data handling
    - Common view test patterns
    """

    def _get_base_url(self) -> str:
        """
        Get the base URL namespace for views.

        Override this or set self.base_url in your test class.

        Returns:
            Base URL string (e.g., "plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_url_name }}")
        """
        if hasattr(self, 'base_url'):
            return self.base_url
        raise NotImplementedError("Set self.base_url or override _get_base_url()")

    def _get_url(self, action: str, instance=None) -> str:
        """
        Get URL for a specific action.

        Args:
            action: Action name (e.g., 'list', 'add', 'edit', 'delete')
            instance: Model instance (required for 'edit', 'delete', detail views)

        Returns:
            URL string
        """
        base_url = self._get_base_url()

        if action in ('add', 'list'):
            return reverse(f"{base_url}_{action}")
        elif action in ('edit', 'delete') and instance:
            return reverse(f"{base_url}_{action}", kwargs={'pk': instance.pk})
        elif instance:
            return reverse(base_url, kwargs={'pk': instance.pk})
        else:
            raise ValueError(f"Invalid action '{action}' or missing instance")

    def post_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Convert test data dictionary to POST-friendly format.

        Converts model instances to PKs, handles many-to-many fields.

        Args:
            data: Dictionary with field names and values

        Returns:
            Dictionary ready for form POST
        """
        post_data = {}

        for key, value in data.items():
            # Handle model instances (foreign keys)
            if hasattr(value, 'pk'):
                post_data[key] = value.pk

            # Handle lists (many-to-many)
            elif isinstance(value, (list, tuple)):
                post_data[key] = [
                    obj.pk if hasattr(obj, 'pk') else obj
                    for obj in value
                ]

            # Handle regular values
            else:
                post_data[key] = value

        return post_data


class PluginGraphQLTestCase(PluginTestCase):
    """
    Base test case for GraphQL query testing.

    Provides:
    - GraphQL query execution helpers
    - Query result validation
    """

    def execute_query(self, query: str, variables: dict | None = None):
        """
        Execute a GraphQL query.

        Args:
            query: GraphQL query string
            variables: Optional query variables

        Returns:
            Dict with GraphQL response data
        """
        url = reverse('graphql')
        data = {'query': query}
        if variables:
            data['variables'] = variables

        response = self.client.post(
            url,
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        return response.json()

    def assertGraphQLSuccess(self, response):
        """Assert that GraphQL query succeeded without errors."""
        json_data = response.json()
        self.assertNotIn('errors', json_data,
                        f"GraphQL query failed: {json_data.get('errors')}")

    def assertGraphQLHasData(self, response, expected_count: int | None = None):
        """
        Assert that GraphQL response contains data.

        Args:
            response: GraphQL response
            expected_count: Optional expected number of results
        """
        self.assertGraphQLSuccess(response)
        json_data = response.json()
        self.assertIn('data', json_data)

        if expected_count is not None:
            # Assuming the query returns a list
            data_key = list(json_data['data'].keys())[0]
            actual_count = len(json_data['data'][data_key])
            self.assertEqual(actual_count, expected_count,
                           f"Expected {expected_count} results, got {actual_count}")


__all__ = [
    'PluginTestCase',
    'PluginModelTestCase',
    'PluginAPITestCase',
    'PluginViewTestCase',
    'PluginGraphQLTestCase',
]
