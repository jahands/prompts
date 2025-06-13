<git-commit-guidelines>

<title>Git Commit Guidelines</title>

<overview>
When making changes to code, commit your changes incrementally as you work. Follow these commit conventions:
</overview>

<commit-format>

```
<type>: <subject>

<body>
```

</commit-format>

<types>

- feat: New feature or functionality
- fix: Bug fix
- chore: Maintenance tasks, dependency updates, configuration changes
- docs: Documentation only changes
- style: Code style/formatting changes (no functional changes)
- refactor: Code restructuring without changing functionality
- test: Adding or modifying tests
- perf: Performance improvements
</types>

<rules>

<rule name="subject-line">

- Maximum 90 characters
- Start with lowercase
- No period at the end
- Use imperative mood ("add" not "adds" or "added")
</rule>

<rule name="body">

- Separate from subject with blank line
- Wrap at 72 characters
- Explain what and why, not how
- Only include when the change requires context
</rule>

<rule name="commit-frequency">

- Commit after each logical unit of change
- Each commit should represent one coherent change
- Don't bundle unrelated changes
</rule>
</rules>

<examples>
<example type="good">
```
feat: add user authentication middleware

Implements JWT-based authentication for API routes.
Includes token validation and refresh logic.
```
</example>

<example type="good">
```
fix: resolve null pointer in user lookup
```
</example>

<example type="good">
```
chore: update dependencies to latest versions
```
</example>

<example type="bad">
```
feat: added new feature to the application that allows users to authenticate using JWT tokens and also fixed some bugs and updated dependencies
```
</example>

<example type="bad">
```
fix: Fixed bug.
```
</example>
</examples>

<key-principles>

- Be concise but descriptive
- One commit = one logical change
- Commit message should make sense without looking at the code
- Skip the body if the subject line is self-explanatory
</key-principles>

</git-commit-guidelines>
