## Security Guidelines

- **Never hardcode** Jira API tokens in source code or skill files
- **Always use** environment variables or a secrets manager
- **Add `.env`** to `.gitignore` in every project
- **Rotate tokens** immediately if exposed in git history
- **Use least-privilege** API tokens scoped to required projects
- **Validate** that credentials are set before making API calls — fail fast with a clear message