# 1. Get available transitions
jira_curl \
  "$JIRA_URL/rest/api/3/issue/PROJ-1234/transitions" | jq '.transitions[] | {id, name: .name}'