---
name: global-model-selection
title: "Global Model Selection Rehberi"
description: >
  40+ benchmark üzerinden Claude (Fable/Opus/Sonnet), GPT, Gemini, DeepSeek,
  Kimi, GLM, Qwen, MiniMax, Grok modellerini göreve göre karşılaştırma ve
  seçme rehberi. Güncel: 9 Haziran 2028.
tags: [model-selection, benchmark, llm-comparison, claude, gpt, gemini, deepseek, fable, grok]
category: mlops
related_skills: [hibrit-ai-yonlendirme-kurali, model-benchmark]
---

# Global Model Selection Rehberi

## Ne İşe Yarar

Kullanıcı "şu iş için hangi modeli kullanmalıyım?" dediğinde, güncel benchmark
verilerine dayanarak hangi modelin o görev için en iyi olduğunu söyler.
Kapsar: Claude (Fable, Opus, Sonnet, Mythos), GPT-5.x, Gemini 1.5/3.x, Kimi, GLM,
Qwen, DeepSeek V4/V3, MiniMax, Grok.

**Güncelleme:** 9 Haziran 2028 — 40+ benchmark, 17+ model.

## Ne Zaman Kullanılır

- Kullanıcı AI model tavsiyesi istediğinde
- "Hangi model daha iyi?" sorusu geldiğinde
- Bir proje/görev için model seçimi yapılırken
- Yeni model çıktığında güncelleme için referans

---

## 1. YAZILIM GELİŞTİRME / KODLAMA

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **Genel kod üretimi (SWE-bench Verified)** | **Fable 5** | **%95.5** | Opus 4.8 | %88.6 |
| **Karmaşık patch (SWE-bench Pro)** | **Fable 5** | **%80.3** | Opus 4.8 | %69.2 |
| **Çok dilli kod (SWE-bench Multilingual)** | **Opus 4.8** | **%84.4** | Fable 5 | %80.5 |
| **Multimodal kod (SWE-bench Multimodal)** | **Opus 4.8** | **%38.4** | Fable 5 | %34.5 |
| **Terminal/CLI (Terminal-Bench 2.0)** | **GPT 5.4** | **%82.7** | Gem 3.1 Pro | %81.0 |
| **Terminal/CLI (Terminal-Bench 2.1)** | **Fable 5** | **%88.0** | Opus 4.7 | %83.4 |
| **Frontier/zor kod (FrontierCode Diamond)** | **Fable 5** | **%29.3** | GPT 5.5 | %13.4 |
| **Live coding (LiveCodeBench)** | **Gemini 3.1 Pro** | **%91.7** | DeepSeek V4-Pro | %93.5* |
| **Competitive programming (Codeforces Elo)** | **Qwen Plus** | **3206** | Fable 5 | 3168 |

> *LiveCodeBench'te DeepSeek V4-Pro %93.5 daha yüksek ama Gemini daha güncel.

**Özet:** Genel kodlama → **Fable 5**. Competitive → **Qwen Plus/DeepSeek V4-Pro**.
Terminal/CLI → **GPT 5.4** veya **Fable 5**. Çok dilli/multimodal → **Opus 4.8**.

---

## 2. MATEMATİK

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **AIME 2025** | **Opus 4.8** | **%99.8** | Fable 5 | %98.1 |
| **AIME 2026** | **GPT 5.5** | **%99.2** | Fable 5 | %98.3 |
| **USAMO 2026** | **GPT 5.5** | **%95.2** | Fable 5 | %97.6* |
| **HMMT 2026 Feb** | **GPT 5.5** | **%97.7** | Fable 5 | %96.2 |
| **IMOAnswerBench** | **GPT 5.5** | **%91.4** | Fable 5 | %89.8 |
| **Apex (ileri matematik)** | **Gemini 3.5 Flash** | **%60.9** | Fable 5 | %54.1 |
| **Apex Shortlist** | **Grok 4.20** | **%90.2** | Fable 5 | %85.9 |
| **ArxivMath** | **Fable 5** | **%78.5** | Opus 4.8 | %71.8 |
| **RiemannBench** | **Fable 5** | **%55.0** | Opus 4.8 | %43.0 |

> *Fable 5 USAMO'da daha yüksek (%97.6) ama GPT 5.5 (%95.2) geniş yelpazede lider.

**Özet:** Klasik yarışma → **GPT 5.5**. Araştırma → **Fable 5**.
AIME 2025/özel sınav → **Opus 4.8**. Apex tarzı → **Gemini 3.5 Flash**.

---

## 3. GENEL BİLGİ & AKIL YÜRÜTME

### 3a. Fen & Bilim

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **GPQA Diamond (fen)** | **Gemini 3.1 Pro** | **%94.1** | Opus 4.8 | %93.5 |
| **CritPt (eleştirel)** | **Fable 5** | **%28.6** | Opus 4.6 | %27.1 |
| **SciCode (bilimsel kod)** | **Fable 5** | **%60.2** | GPT 5.4 | %58.9 |
| **Humanity's Last Exam** | **Fable 5** | **%53.3** | Opus 4.7 | %53.1 |
| **Blueprint-Bench 2** | **Fable 5** | **%38.6** | Opus 4.7 | %36.2 |

### 3b. Sağlık & Biyomedikal

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **HealthBench** | **Fable 5** | **%62.7** | Opus 4.8 | %61.1 |
| **HealthBench Professional** | **Fable 5** | **%66.0** | Opus 4.8 | %64.7 |
| **BioMysteryBench (insan)** | **Fable 5** | **%83.9** | Opus 4.7 | %82.6 |
| **BioMysteryBench (zor)** | **Fable 5** | **%46.1** | Opus 4.7 | %40.0 |

### 3c. Bilgi & Gerçeklik

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **MMLU-Pro** | **Gemini 3.1 Pro** | **%91.0** | Fable 5 | %89.1 |
| **MMMLU (çok dilli)** | **Gemini 3.1 Pro** | **%92.6** | Fable 5 | %92.7* |
| **SimpleQA-Verified** | **Gemini 3.1 Pro** | **%75.6** | Kimi K2.6 | %57.9 |
| **Chinese-SimpleQA** | **Gemini 3.1 Pro** | **%85.9** | GLM 5.1 | %84.4 |

### 3d. Soyut Akıl Yürütme (ARC-AGI)

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **ARC-AGI-1** | **Gemini 3.1 Pro** | **%98.0** | DeepSeek V4 | %95.0 |
| **ARC-AGI-2** | **GPT 5.4** | **%85.0** | Gemini 3.1 Pro | %78.8 |
| **ARC-AGI-3** | **Opus 4.8** | **%1.5** | — | (tümü %1.5 altı) |

### 3e. Çok Biçimli & Görsel (Multimodal)

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **MMMU-Pro (çok modal)** | **Gemini 3.5 Flash** | **%83.6** | Fable 5 | %81.2 |
| **CharXiv Reasoning (araçsız)** | **Fable 5** | **%88.9** | Opus 4.8 | %86.1 |
| **CharXiv Reasoning (araçlı)** | **Fable 5** | **%93.5** | Opus 4.8 | %93.2 |
| **ChartQAPro (araçsız)** | **Opus 4.8** | **%69.4** | Fable 5 | %67.6 |
| **ChartQAPro (araçlı)** | **Opus 4.8** | **%72.3** | Fable 5 | %69.8 |

**Özet:** Fen/bilgi/çok modal → **Gemini 3.1 Pro/Flash**. Eleştirel/bio → **Fable 5**.
Soyut akıl (kolay) → **Gemini**. Soyut akıl (zor) → **GPT 5.4**.
Grafik/tablo okuma → **Opus 4.8**.

---

## 4. UZUN BAĞLAM (1M Token)

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **MRCR 1M (belge okuma)** | **Opus 4.8** | **%92.9** | Fable 5 | %89.5 |
| **CorpusQA 1M (külliyat)** | **Opus 4.8** | **%71.7** | Fable 5 | %68.2 |
| **GraphWalks BFS 256K** | **Fable 5** | **%91.1** | Opus 4.8 | %85.9 |
| **GraphWalks Parents 256K** | **Fable 5** | **%99.96** | Opus 4.8 | %99.9 |

> MRCR/CorpusQA'da Opus 4.8 lider, GraphWalks'ta Fable 5 önde.
> Uzun belge + karmaşık ilişki → **Fable 5**. Düz okuma → **Opus 4.8**.

---

## 5. EYLEMCİ / BİLGİSAYAR KULLANIMI (Agent)

### 5a. Tarayıcı & Bilgisayar Kullanımı

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **BrowseComp (tarama)** | **Fable 5** | **%88.0** | Opus 4.8 | %87.9 |
| **OSWorld-Verified (işletim sistemi)** | **Fable 5** | **%85.0** | Opus 4.8 | %85.4* |
| **ScreenSpot-Pro (araçsız)** | **Opus 4.8** | **%82.3** | Fable 5 | %79.5 |
| **ScreenSpot-Pro (araçlı)** | **Opus 4.8** | **%87.9** | Fable 5 | %87.6 |
| **Automation Bench** | **Fable 5** | **%17.4** | Opus 4.7 | %15.5 |

### 5b. Araç & Protokol Kullanımı

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **MCP-Atlas** | **Gemini 3.1 Pro** | **%83.6** | Fable 5 | %82.2 |
| **Toolathlon** | **Gemini 3.1 Pro** | **%56.5** | Fable 5 | %55.6 |
| **τ2-bench (Retail)** | **Fable 5** | **%91.9** | Opus 4.7 | %91.7 |
| **τ2-bench (Telecom)** | **Gemini 3.5 Flash** | **%99.3** | Fable 5 | %99.3* |

### 5c. Alan Agentları (Finans/Hukuk/Ofis)

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **Finance Agent v1.1** | **Opus 4.8** | **%64.4** | Fable 5 | %61.5 |
| **Finance Agent v2** | **Gemini 3.5 Flash** | **%57.9** | Opus 4.8 | %53.9 |
| **Legal Agent (Harvey seti)** | **Fable 5** | **%13.3** | Opus 4.8 | %10.4 |
| **Legal Agent (açık set)** | **Fable 5** | **%16.9** | Opus 4.8 | %13.4 |
| **OfficeQA Pro** | **Fable 5** | **%57.9** | Opus 4.8 | %52.6 |
| **Vending-Bench 2 ($)** | **Opus 4.7** | **$10.937** | Fable 5 | $8.018 |

### 5d. Belge & Ekonomi

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **HLE (araçlı)** | **Fable 5** | **%64.5** | Opus 4.7 | %64.7* |
| **GDPval-AA (Elo)** | **Fable 5** | **1932** | Opus 4.7 | 1890 |
| **GDP.pdf (görsel)** | **Fable 5** | **%29.8** | Opus 4.8 | %24.9 |

**Özet:** Agent/bilgisayar/tarayıcı → **Fable 5** (ezici lider).
Araç/MCP kullanımı → **Gemini 3.1 Pro**. Finans → **Gemini/Ops**.
Ofis/belge → **Fable 5**.

---

## 6. SİBER GÜVENLİK

| Görev | En İyi Model | Skor | 2. Seçenek | Skor |
|-------|-------------|------|-----------|------|
| **CyberGym** | **GPT 5.5** | **%81.8** | Fable 5 | %83.1* |
| **ExploitBench** | **Fable 5** | **%78.0** | Opus 4.8 | %69.0 |

> *CyberGym'de Fable 5 %83.1 daha yüksek ama GPT 5.5 geniş yelpazede lider.

**Özet:** Siber güvenlik → **Fable 5** (exploit) veya **GPT 5.5** (genel).

---

## 7. KAZANÇ TABLOSU (Win Count)

Toplam benchmark galibiyeti (Mythos Preview hariç, 9 Haziran 2028 itibarıyla):

| Sıra | Model | Galibiyet | Güçlü Olduğu Alan |
|------|-------|-----------|-------------------|
| 🥇 | **Fable 5** | **28** | Kod, agent, sağlık, bilim, uzun bağlam, exploit |
| 🥈 | **Gemini 3.1 Pro** | **8** | Bilgi, fen, multimodal, MCP araç |
| 🥉 | **Opus 4.8** | **7** | Multilingual kod, uzun belge, grafik, soyut-3 |
| 4 | **GPT 5.4/5.5** | **7** | Terminal, soyut-2, matematik, güvenlik |
| 5 | **Opus 4.6** | **4** | (çeşitli) |
| 6 | **Gemini 3.5 Flash** | **4** | Finans v2, telecom, multimodal |
| 7 | **DeepSeek V4-Pro** | **3** | Competitive coding |

---

## 8. HIZLI BAŞVURU — GÖREVE GÖRE MODEL

| Yapmak İstediğin | Kullan |
|------------------|--------|
| Kod yazmak / debug | **Fable 5** (veya DeepSeek V4-Pro competitive için) |
| Terminal script / CLI | **GPT 5.4** veya **Fable 5** |
| Competitive programming | **Qwen Plus** (3206 Elo) veya **DeepSeek V4-Pro** |
| Matematik yarışması | **GPT 5.5** |
| Matematik araştırma | **Fable 5** |
| Uzun belge analizi (1M token) | **Opus 4.8** (düz okuma) / **Fable 5** (karmaşık ilişki) |
| Genel bilgi / ansiklopedik | **Gemini 3.1 Pro** |
| Görsel/multimodal işlemek | **Gemini 3.5 Flash** |
| Web/ekran otomasyonu (agent) | **Fable 5** |
| MCP araç kullanımı | **Gemini 3.1 Pro** |
| Bilimsel araştırma / bio | **Fable 5** |
| Soyut akıl (ARC kolay) | **Gemini 3.1 Pro** |
| Soyut akıl (ARC zor) | **GPT 5.4** |
| Grafik/tablo okuma | **Opus 4.8** |
| Finans modeli | **Gemini 3.5 Flash** (v2) / **Opus 4.8** (v1.1) |
| Hukuk / ofis görevleri | **Fable 5** |
| Siber güvenlik (exploit) | **Fable 5** |
| Siber güvenlik (genel) | **GPT 5.5** |
| Görsel akıl yürütme (araçlı) | **Fable 5** (%93.5 CharXiv) |
| Hızlı prototip / ucuz çözüm | **DeepSeek V4** veya **Gemini 3.5 Flash** |

---

## 9. ÖNEMLİ NOTLAR (Pitfalls)

1. **Tek bir "en iyi" model yok.** Fable 5 en çok galibiyete sahip (%70)
   ama Gemini/GPT/DeepSeek belirli nişlerde onu geçiyor.

2. **Benchmark skorları ≠ gerçek dünya.** SWE-bench yüksek puanı her zaman
   günlük kullanımda aynı kalite anlamına gelmez.

3. **Fiyat/performans dengesi.** DeepSeek V4-Pro ve Gemini 3.5 Flash,
   belirli görevlerde çok daha ucuz alternatifler.

4. **Mythos Preview referans modeldir.** Genel kullanıma açık değil,
   karşılaştırmalarda dışarıda tutulmalı.

5. **ARC-AGI-3'te tüm modeller %1.5 altında** — bu seviye için yeni
   benchmark'lar gerekiyor. Henüz hiçbir model çözemedi.

6. **Win count 28 ≠ her şeyde en iyi.** Fable 5 en çok kategoride lider
   ama Gemini 3.1 Pro bilgi/fen/araç kategorilerinde açık ara önde.

---

## Güncelleme

Bu skill, yeni benchmark verileri yayınlandıkça güncellenmeli.

**Son güncelleme:** 9 Haziran 2028
**Güncelleme sıklığı:** Yeni model çıktığında veya büyük benchmark güncellemesi olduğunda.

**Kaynaklar:** 40+ benchmark üzerinden derlenmiştir.

## Referans Dosyaları

Bu skill altında:
- `references/gguf-abliterated-modeller.md` — API modellerinin yerel GGUF/abliterated alternatifleri
