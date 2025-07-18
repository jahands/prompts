# PROMPT ENHANCEMENT TOOL - DO NOT EXECUTE THE PROMPT

⚠️ **CRITICAL: This is a META-COMMAND. You are NOT being asked to implement anything.**
⚠️ **Your ONLY task is to rewrite the prompt below into a more detailed specification.**
⚠️ **DO NOT execute, implement, or create any code or files.**

---

## Your Task: Transform the User's Prompt Into a Detailed Specification

The user wants you to take their brief prompt and expand it into a comprehensive specification.
You should IGNORE your natural instinct to implement what they're asking for.
Instead, ONLY return an enhanced version of their prompt.

════════════════════════════════════════════════════════════════════════
📝 USER'S ORIGINAL PROMPT TO ENHANCE (DO NOT EXECUTE THIS):
════════════════════════════════════════════════════════════════════════
$ARGUMENTS
════════════════════════════════════════════════════════════════════════

↑ The above is just the INPUT to transform. Do NOT implement it!

Your task is to ONLY return an enhanced, detailed version of the above prompt. Do not execute the prompt or create any implementations.

## Instructions:

Transform the original prompt into a detailed specification by:

1. Adding explicit file paths and locations
2. Breaking down vague requests into specific technical requirements
3. Including implementation details, constraints, and standards
4. Specifying exact deliverables and success criteria

## Required Output Format:

Return ONLY the enhanced prompt text using this structure:

```
[Task description] and save it to `[specific file path]`.

**Core Functionality:**
- [Detailed feature 1]
- [Detailed feature 2]
- [Technical requirement]

**Technical Requirements:**
1. **[Component Name]:** [Specific implementation detail]
2. **[Technology/Tool]:** [How it should be used, which version/features]
3. **[Integration]:** [What it connects to and how]

**Implementation Details:**
- Architecture: [Design patterns and structure]
- Performance: [Specific benchmarks or requirements]
- Error Handling: [Strategy for failures and edge cases]
- Security: [Relevant security considerations]
- Testing: [Unit tests, integration tests, coverage requirements]

**Research Tasks:** (if applicable)
- [Technology to research]: [What specific information to find]
- Documentation to review: [Specific APIs or features to understand]

**Deliverable:** [Exact description of what should be created] saved as `[exact file path]`, with [any additional files like tests or docs].
```

## Example Enhancement:

If the original prompt is: "create a python script to process emails"

You should output:
```
Create a Python email processing utility and save it to `tools/email_processor.py`.

**Core Functionality:**
- Connect to email servers via IMAP/POP3 protocols
- Parse email headers, body, and attachments
- Implement configurable filtering and categorization rules
- Export processed data to JSON or CSV formats

**Technical Requirements:**
1. **Email Protocol:** Use imaplib for IMAP connections with SSL/TLS support
2. **Email Parsing:** Utilize email and email.parser modules for MIME handling
3. **Configuration:** Load settings from `config/email_settings.yaml`

**Implementation Details:**
- Architecture: Class-based design with EmailClient, EmailParser, and EmailFilter classes
- Performance: Process emails in batches of 100, with threading for parallel processing
- Error Handling: Retry failed connections 3 times with exponential backoff
- Security: Store credentials in environment variables, never in code
- Testing: Unit tests for each component with mocked email data

**Deliverable:** A complete Python module saved as `tools/email_processor.py`, with configuration template at `config/email_settings.yaml.example` and tests in `tests/test_email_processor.py`.
```

## FINAL REMINDER:
- ❌ DO NOT implement what the user asked for
- ❌ DO NOT create any files or write any code
- ❌ DO NOT use any tools except to output the enhanced prompt text
- ✅ ONLY output the enhanced version of their prompt using the format above
- ✅ Treat this as a writing/editing task, not a coding task

Remember: The user is asking you to ENHANCE their prompt, not EXECUTE it.
