# Test Rule Prompts for Cursor Rules Guide

These 10 test prompts were used to validate the effectiveness of the cursor-rules.mdc guide through test-driven development. They represent a mix of simple and complex rules to ensure the guide works across different complexity levels.

## Simple Rules (Expected <50 lines)

### 1. Indentation Rule
"Write a rule for always using 2 spaces for indentation in JavaScript/TypeScript files, never tabs"

### 2. Error Messages Rule
"Write a rule that tells the LLM to always provide error messages with context about what the user was trying to do and suggest a fix"

### 3. Async Error Handling Rule
"Write a rule that says to always use try-catch blocks for async operations and to log errors with structured logging that includes timestamp, error type, and user context"

### 4. Naming Conventions Rule
"Write a rule for using camelCase for variables and functions, PascalCase for classes and types, and UPPER_SNAKE_CASE for constants"

### 5. Comment Style Rule
"Write a rule that says to avoid obvious comments like '// increment counter' and instead write comments that explain why something is done, not what is done"

### 6. Import Ordering Rule
"Write a rule for organizing imports: external packages first, then internal modules, then relative imports, with blank lines between each group"

## Complex Rules (Expected to use fuller structure)

### 7. Dependency Injection Rule
"Write a rule for implementing dependency injection in TypeScript classes, including when to use constructor injection vs property injection, and how to handle circular dependencies"

### 8. React Organization Rule
"Write a rule for organizing React components - keep components under 200 lines, extract hooks to separate files, and colocate tests with components"

### 9. API Design Rule
"Write a rule for designing RESTful APIs including resource naming, HTTP method usage, status codes, error response format, pagination strategies, and versioning approaches"

### 10. Testing Strategy Rule
"Write a rule for comprehensive testing practices including unit test structure, integration test patterns, test naming conventions, mocking strategies, test data management, and coverage requirements"

## Usage

To test a cursor rules guide:

1. Use these prompts with the Task tool to spawn sub-agents
2. Have each sub-agent read the guide and create a rule
3. Analyze the generated rules for appropriate complexity
4. Simple rules should stay minimal (<50 lines)
5. Complex rules may legitimately need additional structure

## Expected Outcomes

- **Simple rules (1-6)**: Should use minimal structure - just title, rules list, and maybe a few concise examples
- **Complex rules (7-10)**: May benefit from overview, key-concepts, or multiple rule blocks due to interconnected concepts
- **Success metric**: 80%+ of rules should have appropriate complexity for their content