# AGENTS.md

## Project

This is a Django online quiz system. Before proposing changes, inspect:

- `quizzes/views.py`, `quizzes/urls.py`, and `quizzes/tests.py`;
- models in `quizzes/models/`;
- the relevant templates in `quizzes/templates/quizzes/`;
- `quizzes/static/quizzes/css/style.css` and `quizzes/static/quizzes/js/main.js`;
- `quiz_system/settings.py` when a setting affects the requested UI behavior.

## Scope

The task is a UI improvement. Prefer changing only:

- the relevant Django templates;
- `quizzes/static/quizzes/css/style.css` and, when needed, `main.js`;
- `quizzes/views.py` or `quizzes/urls.py` only when the interface needs data or a small UI-related interaction;
- tests for the changed behavior.

Do not change models, create migrations, add dependencies, replace the application design, or modify unrelated files unless the user explicitly approves this after you explain why it is necessary.

## Development rules

- Preserve the existing Django project structure and Ukrainian interface language.
- Reuse the existing base template and CSS style where it is reasonable; keep the result visually consistent and responsive.
- Keep server-side behavior safe: do not trust values from the browser that affect quiz results or access to data.
- Use semantic HTML, visible labels, keyboard-accessible controls, and readable colour contrast.
- Do not add API keys, secrets, external tracking, remote fonts, or network-dependent assets.
- Keep the change focused on the assigned User Story.

## Workflow

1. First report your findings and a concise implementation plan. Do not edit files yet.
2. Wait for explicit approval of the plan before implementation.
3. After implementation, report changed files and the verification result.

## Testing

Add or update Django tests for the behavior that is practical to test at the view/template level. Do not claim that visual styling is covered by unit tests.

Run:

`python manage.py test`

Report the command and its result. Also state what UI scenario should be checked manually in a browser.
