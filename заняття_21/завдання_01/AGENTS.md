# AGENTS.md

## Project

This is a Django blogging platform.

Before making changes, inspect:

- `blog/models.py`
- `blog/views.py`
- `blog/forms.py`
- `blog/urls.py`
- `blog/tests.py`
- relevant templates in `blog/templates/`
- `blogsite/settings.py`

## Scope

You may change:

- files inside `blog/`;
- Django migrations related to the requested feature;
- project documentation when required.

Do not modify unrelated static assets or vendor files.

## Development rules

- Preserve the existing Django project structure.
- Use the existing authentication and role system.
- Enforce permissions on the server side, not only in templates.
- Use Django timezone utilities for dates and publication times.
- Keep migrations small and related to the requested feature.
- Do not add dependencies unless the feature cannot reasonably be implemented without them.
- Do not add secrets, credentials, or API keys.

## Testing

Add tests for new behavior in `blog/tests.py` or an appropriate test module.

Run:

`python manage.py test`

Report:

- files changed;
- migrations created;
- tests added;
- verification command and result.