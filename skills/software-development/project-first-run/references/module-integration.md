# Multi-Module Integration Patterns

## The Pattern

A Python project that has 4+ independent modules (dashboard, telegram bot, notion writer, LLM provider) needs:
1. A shared `.env` at the root level
2. A unified `start.py` orchestrator that launches all modules
3. Proper `__init__.py` in each module directory
4. An import chain from the main entry point to each module

## Integration Checklist

- [ ] All module directories exist under the project root
- [ ] Each module has `__init__.py` (for explicit imports)
- [ ] Root `.env` contains ALL environment variables needed by ALL modules
- [ ] Sub-module `.env` files exist only as optional overrides (or removed entirely)
- [ ] `start.py` loads root `.env` before any sub-module imports
- [ ] Module-level `requirements.txt` files are aggregated into root `requirements.txt`
- [ ] Main entry point (main.py) can import all modules
- [ ] Gateway/service layer can launch sub-modules as subprocesses

## Module Directory Structure After Integration

```
proje/
├── main.py                  # ReAct dongusu (ana ajan)
├── start.py                 # Orkestrator (tum servisleri baslatir)
├── gateway_runner.py        # Multi-channel gateway
├── .env                     # ORTAK .env (TUM moduller icin)
├── reyemen.bat              # Windows baslatici
├── requirements.txt         # ORTAK bagimliliklar
├── dashboard/
│   ├── __init__.py          # ✅ ZORUNLU
│   ├── app.py               # FastAPI + HTMX web UI
│   └── data/                # Job verileri
├── llm_provider/
│   ├── __init__.py          # ✅ ZORUNLU
│   ├── provider.py          # OpenAI/Anthropic/Groq/Ollama
│   ├── models.py            # LLMResponse dataclass
│   └── config.yaml          # Provider ayarlari
├── telegram_bot/
│   ├── __init__.py          # ✅ ZORUNLU
│   └── bot.py               # /run, /status, /logs
├── notion_writer/
│   ├── __init__.py          # ✅ ZORUNLU
│   └── notion_writer.py     # Notion API yazma
```

## Subprocess vs In-Process

For production: **subprocess** (start.py launches each module as a separate process).
- ✅ Crash isolation — one module crashing doesn't take down others
- ✅ Independent restart — restart telegram without restarting dashboard
- ✅ Resource separation — each module can have its own memory budget
- ❌ More complex lifecycle management

For development: **in-process threading** (gateway_runner imports modules directly).
- ✅ Simpler debugging
- ✅ Shared state
- ❌ One crash takes everything down
- ❌ GIL contention

## start.py Orchestrator Template

```python
import subprocess, sys, threading, time
from pathlib import Path
from dotenv import load_dotenv

PROJE_KOK = Path(__file__).parent.resolve()
# Load .env ONCE at the very beginning
load_dotenv(PROJE_KOK / ".env", override=True)

class Servis:
    def __init__(self, ad, path, env=None):
        self.ad = ad
        self.path = path
        self.env = env or dict(os.environ)

    def baslat(self):
        self.process = subprocess.Popen(
            [sys.executable, str(self.path)],
            cwd=str(PROJE_KOK),
            env=self.env,
        )

    def durdur(self):
        self.process.terminate()
```

## Gateway Integration

The gateway (gateway_runner.py) manages channels:
- `TerminalChannel` — stdin/stdout interaction
- `TelegramChannel` — subprocess that runs telegram_bot/bot.py
- `WebSocketChannel` — connects to dashboard's WebSocket endpoint

The gateway's `create_default_gateway()` function creates all channels and registers them. This is called from start.py.

## Common Issues

1. **Duplicate `.env` files** — If both root/ and sub-module/ have `.env`, which one takes effect? Solution: root `.env` has ALL vars, sub-module `.env` is for local development only.
2. **Import path confusion** — When `telegram_bot/bot.py` is run as a subprocess, it uses its own `sys.path`. Root imports may fail. Solution: use `sys.path.insert(0, str(PROJE_KOK))` in each module's entry point, or run everything from root.
3. **Port conflicts** — Dashboard (FastAPI) uses port 8080. If another service also binds to 8080, it fails. Solution: make ports configurable via `.env`.
4. **Shared data corruption** — If dashboard and telegram both write to `data/jobs.json`, add a threading lock or use SQLite instead of JSON for shared state.
