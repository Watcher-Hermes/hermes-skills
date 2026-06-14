# Restart server
lms server start --port 1234
```

### GUI'yi Açmak İçin Yeniden Başlatma

```bash
taskkill /F /IM "LM Studio.exe"
sleep 2
start "" "C:\\Users\\marko\\AppData\\Local\\Programs\\LM Studio\\LM Studio.exe"
sleep 8   # GUI'nin açılmasını bekle
```

### Vision Not Available Fallback

When active Hermes model doesn't support `vision_analyze` (confirmed: DeepSeek V4 Flash via nous provider does NOT support vision — `unknown variant 'image_url', expected 'text'` hatası):

- **This is a model limitation, not a tool bug** — the error `unknown variant 'image_url'` means the model only accepts text inputs
- Use Ollama's local vision model (llava-llama3) via `screen-vision-analiz` skill for screenshot analysis
- Or use window config bounds + coordinate-approximation for clicks
- Or use `lms` CLI for model ops instead of GUI automation
- Or ask the user to describe what they see on screen
- Or switch Hermes provider to a vision-capable model temporarily