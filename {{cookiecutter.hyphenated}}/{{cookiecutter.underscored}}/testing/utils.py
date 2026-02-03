"""
Utility functions for testing {{ cookiecutter.project_name }}.

These helpers assist with common testing operations like creating test data,
handling forms, and managing test state.
"""

import random
import string
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


def get_random_string(length: int = 10, charset: str = string.ascii_letters + string.digits) -> str:
    """
    Generate a random string for test data.

    Args:
        length: Length of the string to generate
        charset: Characters to use for generation

    Returns:
        Random string

    Example:
        >>> name = get_random_string(20)
        >>> slug = get_random_string(10, string.ascii_lowercase + string.digits)
    """
    return ''.join(random.choices(charset, k=length))


def create_test_user(username: str | None = None, permissions: list[str | None] = None,
                    is_staff: bool = True, is_superuser: bool = False) -> User:
    """
    Create a test user with optional permissions.

    Args:
        username: Username (defaults to random string)
        permissions: List of permission strings in format "app_label.codename"
        is_staff: Whether user has staff access
        is_superuser: Whether user is a superuser

    Returns:
        User instance

    Example:
        >>> user = create_test_user(
        ...     permissions=['{{ cookiecutter.underscored }}.view_{{ cookiecutter.__model_url_name }}']
        ... )
    """
    if username is None:
        username = f"testuser_{get_random_string(8)}"

    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        is_staff=is_staff,
        is_superuser=is_superuser,
        password="testpass123"
    )

    if permissions and not is_superuser:
        from django.contrib.auth.models import Permission

        for permission_string in permissions:
            app_label, codename = permission_string.split('.')
            permission = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
            user.user_permissions.add(permission)

    return user


def post_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Convert test data dictionary to POST-friendly format.

    Handles:
    - Model instances (converts to PK)
    - Lists of model instances (converts to list of PKs)
    - Regular Python values (passed through)

    Args:
        data: Dictionary with field names and values

    Returns:
        Dictionary ready for form POST

    Example:
        >>> from ..models import {{ cookiecutter.__model_name }}
        >>> obj = {{ cookiecutter.__model_name }}.objects.first()
        >>> form_data = post_data({'name': 'Test', 'related': obj})
        >>> # form_data = {'name': 'Test', 'related': 1}
    """
    post_dict = {}

    for key, value in data.items():
        # Handle None
        if value is None:
            post_dict[key] = value

        # Handle model instances (foreign keys)
        elif hasattr(value, 'pk'):
            post_dict[key] = value.pk

        # Handle lists (many-to-many or multi-select)
        elif isinstance(value, (list, tuple)):
            post_dict[key] = [
                obj.pk if hasattr(obj, 'pk') else obj
                for obj in value
            ]

        # Handle booleans (convert to string for forms)
        elif isinstance(value, bool):
            post_dict[key] = str(value).lower()

        # Handle regular values
        else:
            post_dict[key] = value

    return post_dict


def extract_form_errors(response) -> dict[str, list[str]]:
    """
    Extract form errors from an HTML response.

    Parses the rendered form and extracts field-specific errors.

    Args:
        response: Django response object

    Returns:
        Dictionary mapping field names to lists of error messages

    Example:
        >>> response = self.client.post(url, bad_data)
        >>> errors = extract_form_errors(response)
        >>> self.assertIn('name', errors)
        >>> self.assertEqual(errors['name'], ['This field is required.'])
    """
    from bs4 import BeautifulSoup

    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        errors = {}

        # Find all form fields with errors
        for field in soup.find_all(class_='has-error') or soup.find_all(class_='is-invalid'):
            field_name = None
            field_errors = []

            # Try to find the field name from input/select/textarea
            for input_elem in field.find_all(['input', 'select', 'textarea']):
                if input_elem.get('name'):
                    field_name = input_elem['name']
                    break

            # Find error messages
            for error_elem in field.find_all(class_='error') or field.find_all(class_='invalid-feedback'):
                error_text = error_elem.get_text().strip()
                if error_text:
                    field_errors.append(error_text)

            if field_name and field_errors:
                errors[field_name] = field_errors

        return errors

    except Exception:
        # If parsing fails, return empty dict
        return {}


def disable_warnings(*logger_names: str):
    """
    Context manager to temporarily disable logging warnings.

    Useful for tests that expect certain warnings (like permission denied).

    Args:
        *logger_names: Names of loggers to disable

    Example:
        >>> with disable_warnings('django.request'):
        ...     response = self.client.get(url)  # Expected 403
        ...     self.assertEqual(response.status_code, 403)
    """
    import logging
    from contextlib import contextmanager

    @contextmanager
    def _disable():
        loggers = [logging.getLogger(name) for name in logger_names]
        original_levels = [logger.level for logger in loggers]

        try:
            for logger in loggers:
                logger.setLevel(logging.ERROR)
            yield
        finally:
            for logger, level in zip(loggers, original_levels, strict=True):
                logger.setLevel(level)

    return _disable()


def create_tags(names: list[str]):
    """
    Create multiple tags for testing.

    Args:
        names: List of tag names

    Returns:
        List of Tag instances

    Example:
        >>> from extras.models import Tag
        >>> tags = create_tags(['important', 'urgent', 'review'])
    """
    from extras.models import Tag

    tags = []
    for name in names:
        tag = Tag.objects.create(
            name=name,
            slug=name.lower().replace(' ', '-')
        )
        tags.append(tag)

    return tags


def get_deletable_objects(instances):
    """
    Get related objects that will be deleted along with the given instances.

    Useful for testing cascade deletion behavior.

    Args:
        instances: QuerySet or list of model instances

    Returns:
        Dictionary mapping model names to counts of objects to be deleted

    Example:
        >>> objs = {{ cookiecutter.__model_name }}.objects.filter(name__startswith='test')
        >>> deletions = get_deletable_objects(objs)
        >>> # deletions = {'{{ cookiecutter.__model_name }}': 3, 'RelatedModel': 5}
    """
    from django.contrib.admin.utils import NestedObjects
    from django.db import DEFAULT_DB_ALIAS

    if not hasattr(instances, '__iter__'):
        instances = [instances]

    collector = NestedObjects(using=DEFAULT_DB_ALIAS)
    collector.collect(instances)

    def count_objects(obj_list):
        """Recursively count objects in nested structure."""
        count = 0
        for obj in obj_list:
            if isinstance(obj, list):
                count += count_objects(obj)
            else:
                count += 1
        return count

    deletions = {}
    for model, instances in collector.model_objs.items():
        model_name = model.__name__
        deletions[model_name] = len(instances)

    return deletions


def assert_object_changes(test_case, instance, action: str,
                         user: User | None = None,
                         message: str | None = None):
    """
    Assert that an ObjectChange entry was created for an action.

    Note: This only works if NetBox's change logging is enabled and the model
    inherits from NetBox's ChangeLoggingMixin.

    Args:
        test_case: TestCase instance (for assertions)
        instance: Model instance that was changed
        action: Action type ('create', 'update', 'delete')
        user: User who performed the action
        message: Optional changelog message to verify

    Example:
        >>> from extras.models import ObjectChange
        >>> obj = {{ cookiecutter.__model_name }}.objects.create(name='Test')
        >>> assert_object_changes(self, obj, 'create', user=self.user)
    """
    try:
        from extras.choices import ObjectChangeActionChoices
        from extras.models import ObjectChange

        action_map = {
            'create': ObjectChangeActionChoices.ACTION_CREATE,
            'update': ObjectChangeActionChoices.ACTION_UPDATE,
            'delete': ObjectChangeActionChoices.ACTION_DELETE,
        }

        object_changes = ObjectChange.objects.filter(
            changed_object_type=ContentType.objects.get_for_model(instance),
            changed_object_id=instance.pk,
            action=action_map[action]
        )

        if user:
            object_changes = object_changes.filter(user=user)

        test_case.assertTrue(
            object_changes.exists(),
            f"No ObjectChange found for {action} of {instance}"
        )

        if message:
            change = object_changes.first()
            test_case.assertEqual(
                change.changelog_message,
                message,
                f"Changelog message mismatch: {change.changelog_message} != {message}"
            )

    except ImportError:
        # ObjectChange not available (NetBox not fully set up or old version)
        pass


__all__ = [
    'get_random_string',
    'create_test_user',
    'post_data',
    'extract_form_errors',
    'disable_warnings',
    'create_tags',
    'get_deletable_objects',
    'assert_object_changes',
]
