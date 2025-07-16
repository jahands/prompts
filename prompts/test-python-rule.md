You are testing a cursor rule for Python type annotations. You will:
1. Create a sub-agent to write Python code
2. Review the sub-agent's output for compliance with the rule
3. Report on how well the rule guided the sub-agent

Use the Task tool to create a sub-agent with this exact prompt:

```
You are writing Python 3.9+ code. First, read the type annotation guidelines at /Users/jh/src/prompts/cursor-rules/python.mdc

Then create a Python module that demonstrates proper type annotations for:
1. A function that takes a list of strings and returns a dictionary mapping strings to their lengths
2. A function that processes optional user data and returns a set of unique IDs
3. A class using TypedDict for user profiles with name, age, and optional email
4. A function accepting multiple collection types (list, set, tuple) and returning their combined length
5. A protocol defining a drawable interface with a draw() method

Write your code to: /tmp/test-python-annotations.py

Make sure to show proper imports and type annotations throughout.
```

After the sub-agent completes, read the generated file at /tmp/test-python-annotations.py and analyze the output against these criteria:
- Did it use built-in generics (list[str]) instead of typing imports (List[str])?
- Did it avoid importing List, Dict, Set, Tuple, Type from typing?
- Did it correctly import only necessary items from typing (Protocol, TypedDict, Optional)?
- Is the code properly annotated throughout?
- Are there any violations of PEP 585?

Report your findings in this format:

## Python Type Annotations Rule Test Results

### Rule Compliance
- ✅/❌ Used built-in generics (list[], dict[], set[], tuple[])
- ✅/❌ Avoided deprecated typing imports (List, Dict, Set, Tuple, Type)
- ✅/❌ Only imported necessary typing items
- ✅/❌ Consistent modern annotations throughout

### Specific Observations
[List any specific good patterns or violations found]

### Overall Assessment
[Brief summary of whether the rule successfully guided the sub-agent]

### Example Code Snippets
[Show 1-2 key examples from the generated code that demonstrate compliance or violations]

Good patterns to look for:
```python
def get_lengths(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

from typing import TypedDict, Optional, Protocol
```

Violations to watch for:
```python
from typing import List, Dict  # Should not import these
def bad_function(items: List[str]) -> Dict[str, int]:  # Should use list[str], dict[str, int]
```