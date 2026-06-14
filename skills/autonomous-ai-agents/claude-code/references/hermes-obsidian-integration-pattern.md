# Claude Code ↔ Hermes + Obsidian Integration Pattern

Created: 2026-06-11 (v1 via Claude Code Opus 4.8 in Agent mode, hermes_v7 project)
Updated: 2026-06-11 (v2 via Hermes Agent, project-agnostic, Windows-proven)

## The Problem

Claude Code (VS Code Agent mode) had no access to Hermes Agent's ~200 skills or Obsidian vault's ~400+ notes. User wanted Claude to read these resources when coding or answering questions.

## The Solution (v2 — Current)

A 3-layer integration at the user home root (project-agnostic):

### Layer 1: VS Code Instructions (.vscode/)

**`.vscode/.instructions.md`** — Context file Claude reads automatically. Tells Claude:
- Hermes skills are at `docs/hermes-skills/` (NTFS junction)
- Obsidian vault is at `docs/obsidian-vault/` (NTFS junction)
- Search these before asking for more info
- Claude Code'a sorarken: "Projenin `docs/hermes-skills` ve `docs/obsidian-vault` klasörlerine erişimin var."

**`.vscode/pre_prompt.md`** — Reusable pre-prompt templates:
- Short: "You have access to `docs/hermes-skills` and `docs/obsidian-vault`. Search before answering."
- Full: Includes searching skills, vault notes, and MCP server usage order.

### Layer 2: NTFS Junctions (docs/)

```cmd
mklink /J C:\Users\marko\docs\hermes-skills    C:\Users\marko\AppData\Local\hermes\skills
mklink /J C:\Users\marko\docs\obsidian-vault   C:\Users\marko\OneDrive\Belgeler\Obsidian Vault
```

Windows NTFS junctions work WITHOUT admin rights (unlike symlinks). Claude Code can browse these via Agent mode's file tree. No API key needed, no server.

### Layer 3: MCP Server (mcp_server/)

**`mcp_server/app.py`** — Flask HTTP server on port 5678:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Status + timestamp |
| `/note?path=<relpath>` | GET | Fetch individual note content |
| `/search?q=<term>` | GET | Search notes (line-by-line substring) |
| `/skills` | GET | List all 200+ skills (cached 60s) |
| `/skill?name=<name>` | GET | Get individual skill SKILL.md |
| `/refresh` | POST | Clear cache |

Features:
- No external deps beyond Flask
- No sklearn/TF-IDF dependency needed
- Cached skills list with 60s TTL
- Path traversal protection
- 20-result limit per search

## Windows-Specific Pitfalls (v2)

### Python Version Issue
- `python` in bash resolves to Hermes venv Python 3.11.15
- Flask must be installed with global Python 3.14 at:
  `***REMOVED-BASE64***-3.14-64/python.exe`
- The Hermes venv's pip is broken (`ModuleNotFoundError: pip._vendor.cachecontrol`)
- Run MCP server with: `***REMOVED-BASE64***-3.14-64/python.exe app.py`

### NTFS Junction Creation
- From bash/cmd.exe, junction creation output often hidden (cmd banner only)
- Use Python subprocess for reliable junction creation:
  ```python
  subprocess.run(['cmd', '/c', 'mklink', '/J', target, source], capture_output=True)
  ```
- Junctions work WITHOUT admin rights; symlinks (/D) require admin

## Windows-Specific Pitfalls (v2)

### Python Version Issue
- `python` in bash resolves to Hermes venv Python 3.11.15
- Flask must be installed with global Python 3.14 at:
  `***REMOVED-BASE64***-3.14-64/python.exe`
- The Hermes venv's pip is broken (`ModuleNotFoundError: pip._vendor.cachecontrol`)
- Run MCP server with: `***REMOVED-BASE64***-3.14-64/python.exe app.py`

### NTFS Junction Creation
- From bash/cmd.exe, junction creation output often hidden (cmd banner only)
- Use Python subprocess for reliable junction creation:
  ```python
  subprocess.run(['cmd', '/c', 'mklink', '/J', target, source], capture_output=True)
  ```
- Junctions work WITHOUT admin rights; symlinks (/D) require admin

### Sending Text to Claude Code in VS Code
The pyautogui.click-based approach (clicking at fixed coordinates) is fragile. The reliable approach:

```python
# 1. Focus VS Code window
import ctypes, subprocess, time
def find_window(title_pattern):
    hwnds = []; user32 = ctypes.windll.user32
    def enum_cb(h, _):
        buf = ctypes.create_unicode_buffer(user32.GetWindowTextLengthW(h) + 1)
        user32.GetWindowTextW(h, buf, len(buf))
        if title_pattern.lower() in buf.value.lower(): hwnds.append(h)
        return True
    WNDP = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(WNDP(enum_cb), 0)
    return hwnds[0] if hwnds else None

hwnd = find_window("Visual Studio Code")
if hwnd:
    user32.ShowWindow(hwnd, 9); time.sleep(0.3)
    user32.SetForegroundWindow(hwnd); time.sleep(0.5)

# 2. Open Claude panel (Ctrl+Shift+I)
subprocess.run(['powershell','-NoProfile','-Command',
    '[System.Windows.Forms.SendKeys]::SendWait("^+i")'], timeout=5)
time.sleep(2)

# 3. Paste from clipboard
subprocess.run(['powershell','-NoProfile','-Command',
    'Get-Content "C:\\Users\\marko\\Desktop\\_cliptmp.txt" | Set-Clipboard'], timeout=5)
subprocess.run(['powershell','-NoProfile','-Command',
    '[System.Windows.Forms.SendKeys]::SendWait("^v{ENTER}")'], timeout=5)
```

PowerShell SendKeys is more reliable than ctypes keybd_event for Electron-based apps like VS Code.
See `mouse-klavye-ctypes` skill for full details.

### How to Test
```bash
# Test junctions
ls /c/Users/marko/docs/hermes-skills/ | head -5
ls /c/Users/marko/docs/obsidian-vault/ | head -5

# Test MCP server (after starting)
curl http://127.0.0.1:5678/health
curl "http://127.0.0.1:5678/search?q=claude"
curl "http://127.0.0.1:5678/skills" | python -c "import json,sys; d=json.load(sys.stdin); print(f'Count: {d[\"count\"]}')"
curl "http://127.0.0.1:5678/skill?name=obsidian" | python -c "import json,sys; d=json.load(sys.stdin); print(f'Skill: {d[\"name\"]}, Size: {d[\"size\"]}B')"
```

## How This Differs from v1

| Aspect | v1 (hermes_v7) | v2 (Hermes Agent, current) |
|--------|----------------|---------------------------|
| Project root | hermes_v7/ | C:\Users\marko\ (agnostic) |
| Symlink type | Unix symlinks | NTFS junctions (Windows-native) |
| MCP port | 7070 | 5678 |
| Search backend | TF-IDF (sklearn) | Substring (no deps) |
| Skill access | Via server only | Junction + server both |
| Dependencies | Flask + sklearn | Flask only |
| Created by | Claude Code Opus 4.8 | Hermes Agent (DeepSeek) |

## Obsidian Note

A permanent record was saved to:
`Hermes Memories/2026-06-11 Claude integration.md`

Contains full integration details and usage instructions.

## When to Use This Pattern

Apply when:
- Setting up Claude Code to access Hermes context in any project
- User asks "can Claude see my skills/notes?"
- Rebuilding after a fresh Hermes install
- Need a project-agnostic integration (not tied to one repo)
