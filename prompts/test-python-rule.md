<test-python-type-annotations-rule>

<title>Test Python Type Annotations Rule</title>

<instructions>
You will test whether the Python type annotations cursor rule effectively guides LLMs to use modern PEP 585 type annotations. Follow these steps exactly:
</instructions>

<step-1>
<description>Create sub-agent to write Python code</description>
<action>
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
</action>
</step-1>

<step-2>
<description>Read and analyze the generated code</description>
<action>
After the sub-agent completes, read the file at /tmp/test-python-annotations.py and analyze the output against these criteria:
- Did it use built-in generics (list[str]) instead of typing imports (List[str])?
- Did it avoid importing List, Dict, Set, Tuple, Type from typing?
- Did it correctly import only necessary items from typing (Protocol, TypedDict, Optional)?
- Is the code properly annotated throughout?
- Are there any violations of PEP 585?
</action>
</step-2>

<step-3>
<description>Report findings</description>
<action>
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
</action>
</step-3>

<reference-patterns>
<good>
```python
def get_lengths(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

from typing import TypedDict, Optional, Protocol
```
</good>

<violations>
```python
from typing import List, Dict  # Should not import these
def bad_function(items: List[str]) -> Dict[str, int]:  # Should use list[str], dict[str, int]
```
</violations>
</reference-patterns>

</test-python-type-annotations-rule>