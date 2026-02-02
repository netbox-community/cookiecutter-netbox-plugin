# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [{{ cookiecutter.version }}] - {% now 'local', '%Y-%m-%d' %}

### Release Summary
Initial release of {{ cookiecutter.project_name }}. This is a **minor** release introducing basic functionality for managing {{ cookiecutter.plugin_name }} resources in NetBox.

### Added
- Initial plugin structure with {{ cookiecutter.__model_name }} model
- Basic CRUD operations through NetBox UI
- Change logging and journaling support
- Custom fields and tags support
{% if cookiecutter.include_rest_api == "yes" -%}
- REST API endpoints for programmatic access
{% endif -%}
{% if cookiecutter.include_graphql == "yes" -%}
- GraphQL support for flexible queries
{% endif -%}
- Comprehensive test suite
- Documentation with MkDocs

### Fixed
- N/A (initial release)

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Security
- N/A (initial release)

---

## Release Notes Template for Future Versions

When creating a new release, use this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Release Summary
Brief narrative summary describing the release type (major/minor/patch) and key highlights.

### **Breaking Changes**
<!-- Only include this section if there are breaking changes -->
- **[#issue]** Description of breaking change and migration path
- Link to detailed migration guide if needed

### Added
- New features and capabilities

### Fixed
- Bug fixes with issue references

### Changed
- Changes to existing functionality

### Deprecated
- Features marked for future removal

### Removed
- Features that have been removed

### Security
- Security improvements and fixes
```

---

**Best Practice**: For clear release communication, ensure each release includes:
1. Narrative summary characterizing the release type (major/minor/patch)
2. Clear indicators for bugs, features, or enhancements
3. Bold "Breaking Changes" header when applicable with migration guidance
4. Detailed changelog with issue references
