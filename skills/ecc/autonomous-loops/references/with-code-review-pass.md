# With code review pass
continuous-claude \
  --prompt "Add authentication feature" \
  --max-runs 10 \
  --review-prompt "Run npm test && npm run lint, fix any failures"