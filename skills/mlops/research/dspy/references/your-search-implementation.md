# Your search implementation
    return results

react = ReAct(SearchQA, tools=[search_tool])
result = react(question="When was Python created?")
```

#### dspy.ProgramOfThought
Generates and executes code for reasoning:

```python
pot = dspy.ProgramOfThought("question -> answer")
result = pot(question="What is 15% of 240?")