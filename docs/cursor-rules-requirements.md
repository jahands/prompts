<cursor-rules-requirements>

<title>Cursor Rules Requirements and Evaluation Criteria</title>

<primary-goal>
Ensure rule complexity matches content complexity - simple concepts should have simple rules, complex concepts can have appropriately complex rules.
</primary-goal>

<line-count-targets>
<simple-rules>
- Target: Under 50 lines total
- Acceptable: 50-60 lines if justified (e.g., comment style needs good/bad examples)
- Failure: Over 60 lines indicates over-structuring
</simple-rules>

<complex-rules>
- Expected: 150-300+ lines
- Justified by: Multiple interconnected concepts, comprehensive examples
- Warning: Under 100 lines might indicate insufficient coverage
</complex-rules>
</line-count-targets>

<structure-requirements>
<simple-rules-must>
- Use only the simple template
- Include ONLY: rules (dash list), minimal examples, title (if adds value)
- NEVER include: context, overview, key-concepts, multiple rule blocks
- No excessive categorization or sections
- Omit <title> when it duplicates the enclosing tag name
</simple-rules-must>

<complex-rules-may>
- Title when it adds specificity beyond the tag name
- Overview section for multi-faceted systems
- Key concepts for new technical terms
- Multiple rule blocks for different contexts
- Extensive examples showing different patterns
- Additional sections like best-practices, anti-patterns
</complex-rules-may>

<title-guidelines>
- OMIT when redundant: <indentation-standards> doesn't need <title>Indentation Standards</title>
- OMIT when obvious: <error-handling> doesn't need <title>Error Handling</title>
- INCLUDE when adding value: <comment-style> → <title>Write Comments That Explain Why, Not What</title>
- INCLUDE in complex rules: Often needed when there's an <overview> section
</title-guidelines>
</structure-requirements>

<example-guidelines>
<simple-rules>
- ONE example is usually sufficient
- Examples should be under 15 lines each
- Only add bad examples if mistake is non-obvious
- Never show variations of same concept
</simple-rules>

<complex-rules>
- Multiple examples acceptable IF each shows fundamentally different pattern
- Examples can be longer to demonstrate complexity
- May include both good and bad examples
- Should cover different use cases
</complex-rules>
</example-guidelines>

<success-metrics>
<per-test-run>
- Target: 80%+ of rules have appropriate complexity
- Good: 90%+ success rate
- Excellent: 95-100% success rate
</per-test-run>

<common-failures>
- Simple rules with unnecessary sections
- Multiple examples showing same concept
- Over-explanation in simple rules
- Complex template used for simple concepts
- Excessive line counts for basic formatting rules
- Redundant <title> tags that duplicate the enclosing tag name
</common-failures>
</success-metrics>

<specific-rule-evaluations>
<formatting-rules>
- Must be under 50 lines
- One clear example only
- No context or overview needed
- Examples: indentation, spacing, brackets
</formatting-rules>

<naming-convention-rules>
- Must be under 50 lines
- One comprehensive example showing all conventions
- Simple list of requirements
- Examples: camelCase, PascalCase, UPPER_SNAKE_CASE
</naming-convention-rules>

<error-handling-rules>
- May be 50-80 lines if including structured format
- One or two examples maximum
- Focus on pattern, not variations
- Examples: try-catch, error messages, logging
</error-handling-rules>

<architectural-rules>
- 150-300+ lines expected
- Multiple sections justified
- Comprehensive examples needed
- Examples: dependency injection, API design, testing strategy
</architectural-rules>
</specific-rule-evaluations>

<analysis-checklist>
<structure-analysis>
- Which rules included unnecessary sections?
- Were simple rules over-structured?
- Did complex rules have appropriate depth?
</structure-analysis>

<example-analysis>
- How many examples did each rule include?
- Were multiple examples justified?
- Could examples be more concise?
</example-analysis>

<line-count-analysis>
- What percentage met line count targets?
- Which rules were significantly over/under?
- Is there a pattern to violations?
</line-count-analysis>

<pattern-recognition>
- What sections appear most often unnecessarily?
- Do certain rule types consistently over-structure?
- What guide elements might be causing issues?
</pattern-recognition>
</analysis-checklist>

<iteration-success-criteria>
- 80%+ of simple rules are under 50 lines
- No simple rules include unnecessary sections
- Complex rules appropriately use fuller structure
- Examples are concise and justified
</iteration-success-criteria>

<red-flags>
- Simple rules consistently exceed 80 lines
- Every rule includes context/overview sections
- Multiple examples appear in basic formatting rules
- Success rate drops below 60%
- Same structural mistakes repeated across iterations
</red-flags>

<analysis-process>
<steps>
1. Run test batch with 5-10 diverse rule prompts
2. Analyze each generated rule against these criteria
3. Calculate success percentages
4. Identify patterns in failures
5. Form hypotheses about guide improvements
6. Document findings in commit message
7. Iterate until success criteria are met
</steps>

<analysis-format>
```
Iteration X Results:
- Simple rules meeting targets: X/Y (X%)
- Average line count for simple rules: XX
- Unnecessary sections found: [list]
- Example count issues: [list]
- Success rate: X%
- Key finding: [pattern observed]
- Hypothesis: [why this happened]
```
</analysis-format>
</analysis-process>

<evaluation-examples>
<good-simple-rule>
- Title: JavaScript Indentation
- Lines: 31
- Sections: title, rules, one example
- Verdict: PASS - appropriate structure
</good-simple-rule>

<bad-simple-rule>
- Title: Variable Naming
- Lines: 82
- Sections: title, context, overview, rules, 3 examples
- Verdict: FAIL - over-structured with unnecessary sections
</bad-simple-rule>

<good-complex-rule>
- Title: Dependency Injection in TypeScript
- Lines: 239
- Sections: title, overview, key-concepts, multiple rules, examples
- Verdict: PASS - complexity matches content
</good-complex-rule>
</evaluation-examples>

</cursor-rules-requirements>