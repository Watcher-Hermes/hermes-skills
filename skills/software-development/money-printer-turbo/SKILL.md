---
name: money-printer-turbo
description: >
title: "Money PRinter Turbo"
  Set up and run harry0703/MoneyPrinterTurbo — AI video generation tool with
  FastAPI backend and Streamlit WebUI. Covers uv dependency management, API key
  configuration, backend startup, and WebUI launch.
platforms: [windows]
triggers:
  - user clones or mentions MoneyPrinterTurbo
  - user says "MoneyPrinter" or "video generator" or "harry0703"
  - repo has config.toml, pyproject.toml, uv.lock

audience: contributor
tags: [coding, development]
category: software-development---

# MoneyPrinterTurbo Setup

**Repo:** https://github.com/harry0703/MoneyPrinterTurbo  
**Python:** 3.11 (`.python-version` dosyasında belirtilmiştir)  
**Bu skill'in yanında:**  
  - `references/session-2026-06-14.md` — bu oturumdaki tam hata çözümleri ve config çakışması detayı  
  - `templates/make_video.py` — Genel amaçlı sahne bazlı Pexels+MoviePy video oluşturucu  
  - `templates/storyboard_video.py` — Storyboard tarzı metin overlay destekli video  
  - `templates/iki_kita.py` — "İki Kıta Tek Bir Nefes" İstanbul belgesel videosu (9 sahne, 35 sn, 4K)  
  - `templates/simit_ayran.py` — Boğaz manzaralı simit+ayran sahnesi (8 sahne, 42 sn)

## 1. Clone & Structure Check

```bash
cd /c/Users/marko
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
```

Kök dizin yapısı:
```
MoneyPrinterTurbo/
├── app/                    → FastAPI backend
├── webui/                  → Streamlit WebUI (giriş: webui/Main.py)
├── main.py                 → Backend giriş noktası (uvicorn)
├── webui.bat / webui.sh    → WebUI başlatma
├── cli.py                  → CLI arayüzü
├── config.toml             → Yapılandırma
├── config.example.toml     → Şablon
├── requirements.txt        → pip bağımlılıkları (miras)
├── pyproject.toml          → Proje tanımı
├── uv.lock                 → uv ile kilitlenmiş bağımlılıklar
└── .venv/                  → Sanal ortam
```

## 2. Bağımlılıkları Yükleme

**ÖNEMLİ:** `uv.lock` varsa `uv sync` kullan. `pip install -r requirements.txt` ikincildir.

```bash
cd /c/Users/marko/MoneyPrinterTurbo
uv sync
```

`uv sync` şunları yapar:
- `.venv` varsa kontrol eder, eksik paketleri ekler
- `.venv` yoksa oluşturur
- 130+ paketi yükler

### .venv'de pip yoksa sorun değil
MoneyPrinterTurbo `.venv`'i uv ile oluşturulmuş olabilir — pip kurulu olmayabilir.
`uv sync` bunu otomatik çözer.

## 3. Yapılandırma (config.toml)

`config.toml` mevcut değilse `config.example.toml`'dan otomatik kopyalanır.

### LLM Sağlayıcıları

| Provider | Anahtarlar | 
|----------|-----------|
| deepseek | `llm_provider=deepseek`, `deepseek_api_key`, `deepseek_base_url=https://api.deepseek.com`, `deepseek_model_name=deepseek-chat` |
| openai | `openai_api_key`, `openai_model_name=gpt-4o-mini` |
| aihubmix | `aihubmix_api_key`, `aihubmix_model_name` |
| ollama | `ollama_base_url`, `ollama_model_name` |

```toml
[app]
llm_provider = "deepseek"
deepseek_api_key = "sk-..."
deepseek_base_url = "https://api.deepseek.com"
deepseek_model_name = "deepseek-chat"
```

### Video Kaynağı

```toml
pexels_api_keys = ["your-pexels-key"]   # pexels.com/api — ücretsiz
pixabay_api_keys = []                    # pixabay.com/api
video_source = "pexels"                  # pexels/pixabay/coverr/local
```

### Arkaplan Müziği

```toml
bgm_type = "random"    # random/local
bgm_file = ""          # local için dosya yolu
bgm_volume = 0.2
```

## 4. Backend'i Başlatma

```bash
cd /c/Users/marko/MoneyPrinterTurbo
.venv/Scripts/python.exe main.py
```

- **Port:** 8080 (varsayılan, `listen_port` ile değiştir)
- **Host:** 0.0.0.0 (varsayılan, `listen_host` ile değiştir)
- **Dokümantasyon:** http://localhost:8080/docs

Doğrulama:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/docs
# → 200 = çalışıyor
```

### Background Process
```bash
terminal(command="cd /c/Users/marko/MoneyPrinterTurbo && .venv/Scripts/python.exe main.py", background=true)
```

## 5. WebUI'yi Başlatma (Streamlit)

```bash
.venv/Scripts/python.exe -m streamlit run webui/Main.py --server.port=8501 --server.headless=true
```

WebUI giriş noktası `webui/Main.py`'dir.

Alternatif: `webui.bat` — port 8501 doluysa 8502-8599 arasında yedek arar.

Doğrulama:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8501
# → 200 = çalışıyor
```

## 6. Video Oluşturma (CLI)

### Temel Kullanım

```bash
.venv/Scripts/python.exe cli.py \
  --video-subject "Konu başlığı" \
  --video-source pexels \
  --voice-name "tr-TR-EmelNeural" \
  --no-subtitle-enabled
```

**UYARI:** `--voice-name` zorunludur. Config.toml'daki `voice_name` değeri CLI tarafından OKUNMAZ.

### Parametre Tablosu

| Param | Zorunlu | Açıklama |
|-------|---------|----------|
| `--video-subject` | Evet | Video konusu |
| `--voice-name` | **Evet** | TTS ses adı |
| `--video-source` | Hayır | pexels/pixabay/coverr/local (varsayılan: pexels) |
| `--no-subtitle-enabled` | Hayır | Altyazıyı kapatır |
| `--video-terms` | Hayır | Virgülle ayrılmış Pexels arama terimleri |
| `--video-materials` | local için | Local video yolları (`storage/local_videos/` altında) |
| `--stop-at` | Hayır | script/terms/audio/subtitle/materials/video |
| `--video-count` | Hayır | Kaç video (varsayılan: 1) |

### Özel Arama Terimleri (--video-terms)

DeepSeek'in otomatik term üretmesini beklemeden istediğin sahneleri doğrudan arat:

```bash
--video-terms "blonde woman Istanbul,Galata Tower drone view,dolphin jumping seagulls flying"
```

### Seslendirmesiz Video (No-Voice)

`--voice-name "no-voice"` ile TTS tamamen kapatılır. Sessiz oluşturulur, sadece bgm kalır:

```bash
.venv/Scripts/python.exe cli.py \
  --video-subject "Konu" \
  --video-source pexels \
  --voice-name "no-voice" \
  --no-subtitle-enabled
```

Süre `generate_silent_audio()` tarafından otomatik hesaplanır (~61 sn).

### TTS Ses Sağlayıcıları

| Sağlayıcı | Prefix | API Key Gerekli | Örnek |
|-----------|--------|----------------|-------|
| Edge TTS (ücretsiz) | (yok) | Hayır | `tr-TR-EmelNeural` |
| Azure TTS V2 | `-V2` | `azure_api_key` | `tr-TR-EmelNeural-V2` |
| Gemini TTS | `gemini:` | `gemini_api_key` | `gemini:Zephyr-Female` |

**Türkçe Edge TTS sesleri:** `tr-TR-EmelNeural` (kadın), `tr-TR-AhmetNeural` (erkek)

### Local Video Kullanımı

```bash
--video-materials "C:/Users/marko/MoneyPrinterTurbo/storage/local_videos/video1.mp4"
```

Video dosyaları `storage/local_videos/` altında olmalı (güvenlik kısıtlaması).

### Çıktı

`storage/tasks/<task_id>/final-1.mp4`

## 7. Özel Video Pipeline (MoviePy 2.x)

Sahne sırasının tam kontrolü için Pexels API + MoviePy:

1. Her sahne için Pexels API'de video ara (`orientation=portrait`)
2. İndir ve MoviePy 2.x ile birleştir
3. Arkaplan müziği ekle

**MoviePy 2.x API farkları (moviepy==2.2.1):**
- `clip.subclip(t1, t2)` → **`clip.subclipped(t1, t2)`**
- Ses seviyesi: `clip.with_volume_scaled(factor)`
- Ses ekle: `clip.with_audio(audio_clip)`
- Import: `from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips`

Hazır şablonlar:
  - `templates/make_video.py` — Genel amaçlı, sahne bazlı video oluşturucu (4K, Pexels, MoviePy)
  - `templates/storyboard_video.py` — Storyboard tarzı, metin overlay desteği ile

### 4K Upscale (MoviePy ile)

Mevcut videoyu 4K (2160x3840) çözünürlüğe yükseltmek için:

```python
from moviepy import VideoFileClip
v = VideoFileClip("input.mp4")
v = v.without_audio()
v = v.resized(height=3840)
v.write_videofile("output-4k.mp4", codec="libx264", fps=24, threads=8)
```

**Dikkat:** Upscale orijinal kaliteyi artırmaz — kaynak 1080p ise 4K'ya büyütünce yumuşama olur.
Daha iyi sonuç için Pexels'ten yüksek çözünürlüklü kaynak seç (`min_h=2160` filtresi ile).

### Text Overlay (MoviePy TextClip)

Windows'ta MoviePy 2.x ile metin eklerken **Pillow font sorunu** oluşabilir:
`Invalid font Arial, pillow failed to use it with error cannot open resource`

**Çözüm:** Windows fontlarının tam yolunu ver:
```python
from moviepy import TextClip
txt = TextClip(
    text="Merhaba",
    font="C:/Windows/Fonts/arial.ttf",  # tam yol
    font_size=36,
    color="white",
    stroke_color="black",
    stroke_width=2,
    method="caption",
)
```

Veya font kullanmadan sadece görsel+müzik ile devam et (metni sonradan video editöründe ekle).

## 8. Tüm Servisleri Başlatma

Backend ve WebUI **ayrı process'lerdir**, ikisi ayrı ayrı başlatılır:

```bash
# Terminal 1: Backend
cd /c/Users/marko/MoneyPrinterTurbo && .venv/Scripts/python.exe main.py

# Terminal 2: WebUI
.venv/Scripts/python.exe -m streamlit run webui/Main.py --server.port=8501 --server.headless=true
```

Port doluysa:
```bash
netstat -ano | grep ":8501 "
taskkill /F /PID <PID>
# veya toptan:  taskkill /F /IM python.exe
```

## 10. Üçüncü Parti AI Video API'leri

MoneyPrinterTurbo **gerçek AI video üretimi yapmaz** — sadece Pexels/Pixabay gibi stok sitelerden hazır videoları bulup birleştirir. "Maymun simit yerken" gibi spesifik sahneler için AI video API'leri gerekir.

### Kling AI

- **Web:** https://kling.ai  
- **API:** https://kling.ai/dev/api-key  
- **Kayıt:** `.env` → `KLING_ACCESS_KEY`, `KLING_SECRET_KEY`  
- **Özellik:** Text-to-video, image-to-video  

### RunwayML

- **Web:** https://app.runwayml.com  
- **API Docs:** https://docs.dev.runwayml.com/api  
- **API Key formatı:** `key_` ile başlayan 128 hex karakter (toplam 132 karakter)  
- **Kayıt:** `.env` → `RUNWAYML_API_KEY`  
- **API Endpoint:** `api.dev.runwayml.com`  
- **Gerekli Header'lar:**  
  ```
  Authorization: Bearer <key>
  X-Runway-Version: v1
  ```
- **Not:** API key doğru formatta olsa bile endpoint versiyonu/uyumluluk sorunları olabilir. En güvenilir kullanım web arayüzüdür.

### Manim (3Blue1Brown Matematik Animasyonları)

```bash
# MoneyPrinterTurbo venv'ine kurulum
cd /c/Users/marko/hermes-ai
C:/Users/marko/hermes-ai/venv/Scripts/python.exe -m pip install manim
```

Test:
```python
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))
        self.wait(1)
```

Render:
```bash
python -m manim test_scene.py TestScene -ql  # düşük kalite
python -m manim test_scene.py TestScene -qh  # yüksek kalite
```

### API Key'leri .env'ye Kaydetme Pattern'i

```bash
# .env'ye ekle
echo "# Kling AI" >> .env
echo "KLING_ACCESS_KEY=xxx" >> .env
echo "KLING_SECRET_KEY=xxx" >> .env

echo "# RunwayML" >> .env
echo "RUNWAYML_API_KEY=key_xxx" >> .env
```

**UYARI:** `.env`'ye yazarken `***` kullanma — f-string ile SyntaxError'a yol açar.  
**Güvenlik:** Hermes terminal çıktısında API key'leri otomatik maskeler (`***`), dosyaya doğru yazılır.

Ardından Obsidian notu oluştur ve `env_watcher.py` çalıştır:
```bash
cd /c/Users/marko/hermes-ai && python env_watcher.py
```

| Araç | config.toml | Varsayılan |
|------|-------------|-----------|
| FFmpeg | `app.ffmpeg_path` | Sistem PATH |
| ImageMagick | `app.imagemagick_path` | `convert` PATH'te |

FFmpeg yoksa: `winget install FFmpeg` (MoviePy 2.x otomatik indirir ama bazen başarısız olur).

## Pitfalls

1. **.venv'de pip yok** → önemli değil, `uv sync` kullan
2. **`uv sync` "VIRTUAL_ENV mismatch" uyarısı** → zararsız
3. **`voice_name` boş** → Edge TTS hatası. CLI'da her zaman `--voice-name` ver
4. **WebUI'da Gemini sesi seçili** → API key yoksa Edge TTS'e düşer (voice.py'ye yama gerekli)
5. **Config.toml sürekli sıfırlanıyor** → WebUI `save_config()` tüm config'i yeniden yazar; elle eklenen `deepseek_api_key`, `voice_name` silinir, `llm_provider` `"openai"`'a döner. **Çözüm:** CLI kullanmadan önce `taskkill /F /IM python.exe` ile tüm Python'ları öldür (**⚠️ her şeyi kapatır**), config'i düzelt, CLI'ı çalıştır. WebUI kapalıyken config bozulmaz.
6. **Port 8501 dolu** → `--server.port=8510` dene
7. **Backend 8080 bind hatası** → eski process'i öldür
8. **MoviePy 2.x `subclip` AttributeError** → `subclip()` yok, `subclipped()` kullan
9. **Gemini TTS fallback parametre hatası** → `azure_tts_v1(text, voice, rate, file)` 4 parametre alır, 5 değil

## Gemini TTS Fallback Yaması

`app/services/voice.py` dosyasında `tts()` fonksiyonunda `is_gemini_voice` bloğu:

Önce API key kontrol et, yoksa Edge TTS'e düş:

```python
elif is_gemini_voice(voice_name):
    gemini_key = config.app.get("gemini_api_key", "")
    if not gemini_key:
        logger.warning(f"Gemini API key not set, falling back to Edge TTS")
        fallback_voice = "tr-TR-EmelNeural"
        return azure_tts_v1(text, fallback_voice, voice_rate, voice_file)
    # API key varsa normal gemini_tts çağır
    parts = voice_name.split(":")
    if len(parts) >= 2:
        voice = parts[1].split("-")[0]
        return gemini_tts(text, voice, voice_rate, voice_file, voice_volume)
```

**UYARI:** `azure_tts_v1()` 4 parametre alır (voice_volume YOK). 5 parametreyle çağırma TypeError alırsın.

## Third-Party AI Video APIs

Bu araçlar **gerçek AI video üretimi** yapar (text-to-video), MoneyPrinterTurbo'nun stok video birleştirmesinden farklıdır.

### Kling AI
- Web: https://kling.ai | API: https://kling.ai/dev/api-key
- .env: `KLING_ACCESS_KEY`, `KLING_SECRET_KEY`

### RunwayML
- Web: https://app.runwayml.com | API Docs: https://docs.dev.runwayml.com/api
- Key format: `key_` + 128 hex = 132 karakter
- .env: `RUNWAYML_API_KEY`
- Header: `Authorization: Bearer *** `X-Runway-Version: v1`
- Web arayüzü API'den daha kararlı

### Manim
```bash
pip install manim
python -m manim scene.py TestScene -ql
```

## Template'ler

Bu skill ile gelen hazır Python script'leri:
- `templates/make_video.py` — Pexels+MoviePy video oluşturucu
- `templates/storyboard_video.py` — Metin overlay destekli
- `templates/iki_kita.py` — İstanbul belgeseli (9 sahne, 35 sn)
- `templates/simit_ayran.py` — Simit+ayran sahnesi (8 sahne, 42 sn)
