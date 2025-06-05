## Code Comment Guidelines

**Only comment to explain WHY, not WHAT. Comment when code alone cannot convey the full context.**

**Comment when:**

- Explaining non-obvious decisions or business logic
- Documenting workarounds, edge cases, or gotchas
- Adding TODOs or noting limitations
- Clarifying complex algorithms or regex patterns

**Don't comment:**

- Self-evident code (`count++`, `user.name = "John"`)
- What well-named functions/variables already express
- Obvious control flow

**Example:**

```python
# Bad: Redundant
count += 1  # Increment count

# Good: Explains context
count += 1  # Compensate for zero-indexing in UI
```
