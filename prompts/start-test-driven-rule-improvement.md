<start-test-driven-improvement>

<title>Start Test-Driven Rule Improvement</title>

<task>
Improve cursor-rules.mdc using test-driven development to ensure it produces appropriately structured rules - simple concepts should have simple rules, complex concepts can have complex rules.
</task>

<required-files>
- cursor-rules/test-driven-rule-development.mdc - Complete process to follow
- docs/cursor-rules-requirements.md - Success criteria and evaluation metrics  
- docs/test-rules.md - The 10 standard test prompts
- cursor-rules/cursor-rules.mdc - The guide you're improving
</required-files>

<process-overview>
Follow the 8-step process in cursor-rules/test-driven-rule-development.mdc:
1. Clean test directory (CRITICAL - prevents contamination)
2. Create test scenarios (use the 10 prompts from docs/test-rules.md)
3. Get user approval (skip if using standard prompts)
4. Run tests after approval
5. Analyze results
6. Commit test results
7. Revise guide based on data
8. Repeat until satisfied
</process-overview>

<specific-guidance>
<test-directory>
- Location: cursor-rules/test-rules/
- MUST clean before starting: rm -rf cursor-rules/test-rules/
</test-directory>

<sub-agent-template>
```
You need to write an LLM rule. First, read the rule-writing guidelines at /Users/jh/src/prompts/cursor-rules/cursor-rules.mdc, then create a rule following those guidelines.

Your task: [INSERT SPECIFIC RULE REQUEST FROM TEST PROMPTS]

Write the rule to this file: /Users/jh/src/prompts/cursor-rules/test-rules/[FILENAME].mdc
```
</sub-agent-template>

<evaluation>
- Use ALL criteria from docs/cursor-rules-requirements.md
- Follow the analysis format specified there
- Apply the line count targets and structure requirements
- Check against the specific rule evaluations
- Use the provided analysis checklist
</evaluation>
</specific-guidance>

<current-state>
- Iterations completed: 6
- Current success rate: 90%
- Recent improvements: Simple template first, strong example warnings, decision tree
- Continue if: Requirements change or success drops below 80%
</current-state>

<common-issues>
- Simple rules with unnecessary <context>, <overview>, or <key-concepts>
- Multiple examples for basic formatting rules  
- Indentation rules with 2+ examples when 1 suffices
- Line counts over 60 for simple rules
- Complex template used for simple concepts
</common-issues>

<begin>
1. Read all required files
2. Clean test directory completely
3. Run the 10 standard test prompts
4. Analyze using requirements criteria
5. Commit results with analysis
6. Revise guide if needed
7. Repeat until 80%+ success
</begin>

</start-test-driven-improvement>