# 3. Find the WS URL
curl -s http://127.0.0.1:9229/json/list | jq -r '.[0].webSocketDebuggerUrl'