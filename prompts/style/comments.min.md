<code-comment-guidelines>

<title>Code Comment Guidelines</title>

<rules>
- Only comment to explain WHY, not WHAT
- Comment when code alone cannot convey the full context
- Explain non-obvious decisions or business logic
- Document workarounds, edge cases, or gotchas
- Add TODOs or note limitations
- Clarify complex algorithms or regex patterns
- Never comment self-evident code (count++, user.name = "John")
- Never comment what well-named functions/variables already express
- Never comment obvious control flow
</rules>

<examples>
<example type="good">
```python
count += 1  # Compensate for zero-indexing in UI
```
</example>
</examples>

</code-comment-guidelines>