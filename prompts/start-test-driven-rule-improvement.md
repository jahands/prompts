Task: Improve the cursor-rules.mdc guide using test-driven development

Please follow the test-driven rule development process outlined in cursor-rules/test-driven-rule-development.mdc.

Starting point: The cursor-rules guide to improve is already at cursor-rules/cursor-rules.mdc in your repository.

Setup:

1. Work with the existing file at cursor-rules/cursor-rules.mdc
2. Create test outputs at cursor-rules/test-rules/ (or another test directory of your choosing)
3. Commit both the guide and test results together for version history

Goal: The guide should help LLMs write appropriately structured rules - simple concepts should have simple rules, complex concepts can have complex rules. The structure should
match the complexity of the content.

Current problem: When tested today, LLMs consistently over-structured simple rules. For example, a basic indentation rule received unnecessary <context>, <overview>, and
<key-concepts> sections when a simple title and rules list would have been sufficient.

Hypothesis to test: The guide may be inadvertently encouraging complexity by:

1. Showing complex template examples prominently
2. Including sections like "overview" and "context" in examples that get copied even when not needed
3. Not being forceful enough about starting with the simplest possible structure

Suggested test prompts to use:

1. "Write a rule for always using 2 spaces for indentation in JavaScript/TypeScript files, never tabs"
2. "Write a rule that tells the LLM to always provide error messages with context about what the user was trying to do and suggest a fix"
3. "Write a rule for implementing dependency injection in TypeScript classes, including when to use constructor injection vs property injection, and how to handle circular
   dependencies"
4. "Write a rule that says to always use try-catch blocks for async operations and to log errors with structured logging that includes timestamp, error type, and user context"
5. "Write a rule for organizing React components - keep components under 200 lines, extract hooks to separate files, and colocate tests with components"

Expected outcomes:

- Rules 1-2 should need only basic structure (title, rules list, maybe examples)
- Rules 3-5 might legitimately benefit from additional sections like key-concepts or categories
- Success = rule structure matches content complexity

Potential improvements to explore:

- Move complex examples to the end or remove them entirely
- Show the simplest possible template as the default
- Add explicit "STOP HERE" guidance after basic structure
- Consider showing "bad" over-structured examples as deterrents
- Test whether less guidance produces better results than more warnings

Please begin by:

1. Reading the test-driven rule development guide
2. Reviewing the current cursor-rules.mdc file
3. Showing me your test prompts before running the first iteration
