## Emülatör Test Sınırlamaları

- **Sanal mikrofon yok:** Google APIs sistem imajı (`google_apis;x86_64`) SpeechRecognizer'ı destekler ama varsayılan emülatörde sanal ses girişi yoktur. SpeechRecognizer `ERROR_NO_MATCH` veya `ERROR_SPEECH_TIMEOUT` ile döner, hiçbir callback (onResults/onPartialResults) ateşlenmez.
- **Gerçek test:** Fiziksel telefona yükle (USB hata ayıklama) veya emülatöre host mikrofondan ses yönlendirmesi yap.
- **Google servis kontrolü:** `adb shell pm list packages google` ile doğrula