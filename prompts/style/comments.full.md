<code-comment-guidelines>
<title>Code Comment Guidelines</title>

<principle>
Only add comments when they provide value beyond what the code itself communicates. Follow these principles:
</principle>

<do-comment>
- Why decisions were made, not what the code does
- Complex algorithms or non-obvious logic
- Workarounds, edge cases, or potential gotchas
- Business rules or domain-specific context
- TODO items or known limitations
- Function/class documentation (purpose, parameters, return values)
- Regular expressions or complex conditions that aren't self-evident
</do-comment>

<dont-comment>
- Simple variable assignments (Set user name to "John" for userName = "John")
- Obvious control flow (Loop through users for for (user in users))
- Self-documenting code (Increment counter for counter++)
- Type information already clear from the code
- Restating what well-named functions do (Get user by ID for getUserById())
</dont-comment>

<examples>
<example type="bad">
<description>Redundant comments that restate the obvious</description>
```python
# Add 1 to count
count += 1

# Check if user is admin
if user.is_admin:
    # Grant access
    grant_access()
```
</example>

<example type="good">
<description>Comments that add valuable context</description>
```python
# Compensate for zero-indexing in the UI display
count += 1

# Admin check required by compliance policy XYZ-123
if user.is_admin:
    grant_access()  # Bypasses the standard approval workflow
```
</example>
</examples>

<reminder>
Good code with meaningful names often needs fewer comments. Strive to make your code self-documenting first, then add comments only where additional context genuinely helps future readers (including yourself).
</reminder>
</code-comment-guidelines>