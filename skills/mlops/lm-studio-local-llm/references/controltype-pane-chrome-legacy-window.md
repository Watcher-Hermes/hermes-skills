# → "[ControlType.Pane] \"Chrome Legacy Window\" ..."
```

**Known window geometry (from session 14-Jun-2026):**
```
Sol: 708  Üst: 20  Sağ: 1540  Alt: 906
Genişlik: 832  Yükseklik: 886
```
These coordinates are for a ~832x886 window positioned center-left on a 1920x1200 display. Use them for:
- Cropping screenshots before OCR: `img.crop((708, 20, 1540, 906))`
- Targeting mouse clicks at known UI regions within the window

### OCR (Tesseract) ile Model Seçme (Önerilen)

UIA element ağacı kapalı olduğu için OCR ile metin bulma kullanılır:

```bash