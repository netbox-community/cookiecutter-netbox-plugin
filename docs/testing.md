# Testing Infrastructure

The cookiecutter template generates a comprehensive testing infrastructure for your NetBox plugin. This page explains what's included and how to use it.

## What's Generated

### Base Test Classes

The template includes standalone base test classes in `{{ cookiecutter.underscored }}/testing/__init__.py` that you can use without importing from NetBox's internal testing utilities:

- **PluginTestCase** - Base class with user management and permissions
- **PluginModelTestCase** - For testing models with instance comparison
- **PluginAPITestCase** - For testing REST API endpoints
- **PluginViewTestCase** - For testing web views and forms
- **PluginGraphQLTestCase** - For testing GraphQL queries

These classes are designed to be stable and independent of NetBox's internal changes.

### Test Utilities

Helper functions in `{{ cookiecutter.underscored }}/testing/utils.py`:

- `get_random_string()` - Generate random test data
- `create_test_user()` - Create users with permissions
- `post_data()` - Convert dictionaries to form POST format
- `extract_form_errors()` - Parse form validation errors
- `disable_warnings()` - Suppress expected log warnings
- `create_tags()` - Bulk tag creation
- And more...

### Test Configuration

The template generates `testing/configuration.py` with NetBox configuration for testing:

- PostgreSQL database setup
- Redis configuration
- Plugin registration
- Logging configuration

### Example Tests

Comprehensive example tests are included:

- **test_models.py** - Model creation, validation, relationships
- **test_views.py** - Web UI, forms, permissions
- **test_api.py** - REST API endpoints (if enabled)

### CI/CD Workflow

The `.github/workflows/ci.yaml` provides automated testing:

**Stage 1: Lint** (Fail Fast)
- Runs Ruff code quality checks
- Quick feedback (~30 seconds)

**Stage 2: Test** (Comprehensive)
- Tests on Python 3.12, 3.13, 3.14
- PostgreSQL 16 + Redis 7 services
- Parallel test execution
- Migration checks

## Running Tests Locally

### Prerequisites

You need NetBox installed in a development environment. See [NetBox Development Getting Started](https://docs.netbox.dev/en/stable/development/getting-started/).

### Basic Test Execution

From your NetBox directory:

```bash
# Run all plugin tests
python manage.py test your_plugin.tests

# Verbose output
python manage.py test your_plugin.tests -v 2

# Run in parallel (faster)
python manage.py test your_plugin.tests --parallel

# Keep database between runs (faster during development)
python manage.py test your_plugin.tests --keepdb

# Run specific test file
python manage.py test your_plugin.tests.test_models

# Run specific test class
python manage.py test your_plugin.tests.test_models.MyModelTestCase

# Run specific test method
python manage.py test your_plugin.tests.test_models.MyModelTestCase.test_create
```

### Environment Variables

The test configuration supports environment variable overrides:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=netbox
export DB_USER=netbox
export DB_PASSWORD=netbox
export REDIS_HOST=localhost
export REDIS_PORT=6379

python manage.py test your_plugin.tests
```

## Writing Tests

### Example: Model Test

```python
from your_plugin.testing import PluginModelTestCase
from your_plugin.models import MyModel

class MyModelTestCase(PluginModelTestCase):
    @classmethod
    def setUpTestData(cls):
        # Create shared test data
        MyModel.objects.create(name='Test 1')
        MyModel.objects.create(name='Test 2')

    def test_create_model(self):
        instance = MyModel.objects.create(name='Test 3')
        self.assertEqual(instance.name, 'Test 3')
        self.assertIsNotNone(instance.pk)

    def test_model_validation(self):
        # Use assertInstanceEqual for deep comparison
        instance = MyModel.objects.first()
        self.assertInstanceEqual(
            instance,
            {'name': 'Test 1'},
            exclude={'created', 'last_updated'}
        )
```

### Example: API Test

```python
from your_plugin.testing import PluginAPITestCase
from your_plugin.testing.utils import get_random_string

class MyAPITestCase(PluginAPITestCase):
    def setUp(self):
        super().setUp()
        self.add_permissions('your_plugin.view_mymodel', 'your_plugin.add_mymodel')
        self.list_url_name = 'plugins-api:your_plugin-api:mymodel-list'

    def test_create_via_api(self):
        url = self._get_list_url()
        data = {'name': get_random_string(20)}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)
```

### Example: View Test

```python
from your_plugin.testing import PluginViewTestCase
from your_plugin.testing.utils import disable_warnings

class MyViewTestCase(PluginViewTestCase):
    def setUp(self):
        super().setUp()
        self.base_url = 'plugins:your_plugin:mymodel'

    def test_view_without_permission(self):
        url = self._get_url('list')
        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_with_permission(self):
        self.add_permissions('your_plugin.view_mymodel')
        url = self._get_url('list')
        response = self.client.get(url)
        self.assertHttpStatus(response, 200)
```

## Best Practices

1. **Use setUpTestData for shared fixtures** - Faster than setUp()
2. **Test both positive and negative cases** - Success and failure scenarios
3. **Always test permissions** - Without and with proper permissions
4. **Use meaningful test names** - Describe what's being tested
5. **Keep tests isolated** - Tests should not depend on each other
6. **Clean up test data** - Use cleanupSubTest() for multiple scenarios
7. **Test edge cases** - Empty strings, None values, maximum lengths
8. **Use factories/utilities** - Don't repeat object creation code
9. **Test validation** - Both model and form validation
10. **Document complex tests** - Add docstrings explaining purpose

## Continuous Integration

The CI workflow runs automatically on:
- Push to main or develop branches
- Pull requests

Tests must pass before PRs can be merged.

You can view test results in the "Actions" tab of your GitHub repository.

## Troubleshooting

**"No module named 'your_plugin'"**
- Ensure plugin is installed: `pip install -e .`
- Ensure plugin is in PLUGINS list in configuration.py

**"Table does not exist"**
- Run migrations: `python manage.py migrate`

**"Permission denied"**
- Ensure you added required permissions in setUp()
- Check permission strings are correct (e.g., `'app.view_model'`)

**Tests hanging**
- Check database/Redis connectivity
- Ensure services are running
- Check for infinite loops or blocking operations

**Random test failures**
- Check for test interdependencies
- Use `--keepdb` flag carefully (may have stale data)
- Ensure proper transaction cleanup

## Additional Resources

- [TESTING.md](../TESTING.md) - Complete testing guide in generated projects
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [NetBox Plugin Development](https://netboxlabs.com/docs/netbox/plugins/development/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
