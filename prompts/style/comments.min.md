<code-comment-guidelines>
<title>Code Comment Guidelines</title>

<principle>
Only comment to explain WHY, not WHAT. Comment when code alone cannot convey the full context.
</principle>

<comment-when>
- Explaining non-obvious decisions or business logic
- Documenting workarounds, edge cases, or gotchas
- Adding TODOs or noting limitations
- Clarifying complex algorithms or regex patterns
</comment-when>

<dont-comment>
- Self-evident code (count++, user.name = "John")
- What well-named functions/variables already express
- Obvious control flow
</dont-comment>

<example type="bad">
count += 1  # Increment count
</example>

<example type="good">
count += 1  # Compensate for zero-indexing in UI
</example>
</code-comment-guidelines>