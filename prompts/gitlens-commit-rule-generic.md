<commit-message-format>

<title>Commit Message Guidelines for LLM Generation</title>

<analysis-first>
Before writing the commit message, examine the diff and answer:
1. What is the primary change? (Look for the most significant modification)
2. Is this fixing something broken, adding new functionality, or maintaining code?
3. Does this repo contain multiple apps/packages that would benefit from scopes?
</analysis-first>

<format>
- Basic format: `<type>: <summary>`
- With scope (optional): `<type>(<scope>): <summary>`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep summary under 72 characters
- Use lowercase for everything (e.g., `fix: correct parsing logic`)
</format>

<when-to-use-scopes>
Scopes are optional but helpful when:
- Working in a monorepo with multiple apps/packages
- Changes are isolated to a specific module or component
- It helps clarify where the change occurred

Examples: `fix(auth): ...`, `feat(api): ...`, `docs(cli): ...`
</when-to-use-scopes>

<type-selection>
- **feat**: Adding new functionality/capability
- **fix**: Fixing broken behavior 
- **docs**: Only documentation changes (*.md, comments, docstrings)
- **style**: Code formatting only (no logic changes)
- **refactor**: Restructuring code without changing behavior
- **test**: Adding or modifying tests
- **chore**: Dependencies, configs, build process, maintenance
</type-selection>

<commit-patterns-by-type>
<feat-pattern>
Template: `feat: add [what] to [where]` or `feat: implement [capability]`
Include: What capability was added + where/when it applies
Ask yourself: What can users/developers now do that they couldn't before?
</feat-pattern>

<fix-pattern>
Template: `fix: [what was broken] in [where]` or `fix: correct [specific issue]`
Include: What was broken + what now works correctly
Ask yourself: What specific problem does this solve?
</fix-pattern>

<docs-pattern>
Template: `docs: [action] [what] in [where]`
Include: The specific file or section updated
Ask yourself: What documentation is now clearer/more complete?
</docs-pattern>

<chore-pattern>
Template: `chore: [action] [what] to [version]` or `chore: update [config/tool]`
Include: Package names and versions for dependencies
Ask yourself: What maintenance task was performed?
</chore-pattern>
</commit-patterns-by-type>

<body-policy>
<default>Simple changes are title-only, but don't hesitate to add a body for substantial or non-obvious changes</default>

<when-to-add-body>
Think about whether someone scanning the git log would understand:
- **What the change accomplishes** (not just what files changed)
- **Why someone would use this feature** (for new functionality)
- **What behavior changed** (for fixes that aren't obvious)

Ask yourself: "Would I want a one-line explanation if I saw this commit title in a year?"
</when-to-add-body>

<good-reasons-for-body>
- New features/commands that aren't self-explanatory from the title
- Complex refactors that change how something works
- Breaking changes or behavior changes
- Non-obvious bug fixes (what was actually broken?)
- Changes with security/performance implications
</good-reasons-for-body>

<body-requirements>
- Keep to 1-2 lines maximum
- Every line MUST be ≤72 characters (wrap longer lines)
- Explain purpose or behavior, don't repeat the title
- Focus on what/why, not implementation details
</body-requirements>
</body-policy>

<examples-with-reasoning>
<good-examples>
# When diff shows: Added retry mechanism with exponential backoff
✅ `feat: add retry logic for flaky external API calls`
Why good: Specific about what (retry logic) and why (flaky APIs)

# When diff shows: Fixed null reference error in user validation
✅ `fix: handle null email field in user validation`
Why good: States what was broken and where

# When diff shows: Updated configuration documentation
✅ `docs: add environment variable descriptions to README`
Why good: Specific document and what was added

# When diff shows: Dependency update in package manager file
✅ `chore: upgrade typescript to 5.3.2`
Why good: Includes package name and version

# When diff shows: Changes isolated to authentication module
✅ `fix(auth): correct token expiration check`
Why good: Uses scope to clarify the module affected

# When diff shows: New test cases for edge conditions
✅ `test: add edge cases for date parsing logic`
Why good: Specific about what tests were added
</good-examples>

<bad-examples>
# When diff shows: Multiple validation improvements
❌ `fix: improve validation` 
Better: `fix: validate required fields in user registration`

# When diff shows: New API endpoint
❌ `feat: update API`
Better: `feat: add bulk delete endpoint for resources`

# When diff shows: Type definition updates
❌ `chore: update types`
Better: `fix: correct nullable fields in user interface`

# When diff shows: Configuration changes
❌ `chore: update config`
Better: `chore: increase API timeout to 30 seconds`
</bad-examples>

<edge-case-guidance>
- Multiple unrelated changes → Focus on the primary change
- Tiny typo fixes → `fix: correct typo in [specific location]`
- Config changes → Include the config filename
- Reverts → `revert: [original commit message]`
- Dependencies → Always include version numbers
</edge-case-guidance>
</examples-with-reasoning>

<body-examples>
<when-body-helps>
feat: add user import command

Bulk imports users from CSV files with validation and 
duplicate detection (supports up to 10,000 users per file)
</when-body-helps>

<breaking-change>
feat: replace REST API with GraphQL

BREAKING: All API endpoints changed. Update client code to use 
GraphQL queries. See migration guide in docs/api-migration.md
</breaking-change>

<non-obvious-fix>
fix: prevent memory leak in background workers

Workers were accumulating event listeners without cleanup, 
causing memory usage to grow over time
</non-obvious-fix>

<stay-title-only>
feat: add dark mode to dashboard
fix: correct typo in validation message  
chore: upgrade react to 18.2.0
docs: add API examples to README
test: add edge cases for email validation
</stay-title-only>
</body-examples>

<validation-questions>
Before finalizing, ask yourself:
1. Does my commit type match what the code actually does?
2. Can someone understand the change without seeing the diff?
3. Is it under 72 characters?
4. Did I include specific names (files, functions, features)?
5. Would a scope make this clearer? (for monorepos)
</validation-questions>

<final-check>
Read your commit message and imagine you're searching the git log in 6 months.
Would you be able to find this change? Would you know what it did?
If not, add more specific details.
</final-check>

</commit-message-format>