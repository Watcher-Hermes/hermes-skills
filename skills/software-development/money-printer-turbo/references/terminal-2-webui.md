# Terminal 2: WebUI
.venv/Scripts/python.exe -m streamlit run webui/Main.py --server.port=8501 --server.headless=true
```

Port doluysa:
```bash
netstat -ano | grep ":8501 "
taskkill /F /PID <PID>