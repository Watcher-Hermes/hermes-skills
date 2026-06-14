## Routing Rules
1. Parse the user request for intent keywords
2. Match to the Agent Registry trigger column
3. Load the corresponding agent file from `agents/<name>.md`
4. Hand off execution with full context
5. Synthesize and present the result back to the user