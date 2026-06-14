# Silent install (NSIS-based):
Start-Process -FilePath 'C:\Users\marko\Downloads\LM-Studio-0.4.16-2-x64.exe' -ArgumentList '/S' -Wait -NoNewWindow
```

Installed to: `C:\Program Files\LM Studio\LM Studio.exe`

### CLI tool (`lms`)

Installed with LM Studio at: `C:\Users\marko\.lmstudio\bin\lms.exe`
Must be in PATH or called with full path / `export PATH="$PATH:/c/Users/marko/.lmstudio/bin"`

### Model storage

Models directory: `C:\Users\marko\.lmstudio\models\`

LM Studio auto-detects GGUF files in subdirectories under this path.
Structure: `models/<model_name>/<file>.gguf`

---