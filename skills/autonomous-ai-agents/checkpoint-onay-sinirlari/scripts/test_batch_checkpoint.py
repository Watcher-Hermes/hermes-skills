#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_batch_checkpoint.py — Testleri N'er N'er paralel calistir, checkpoint'li.

v2: Checkpoint sistemi — her 10 batch'te bir _test_checkpoint.json'a durum kaydeder.
     Restart'ta kaldigi yerden devam eder (checkpoint okunur, islenmis dosyalar atlanir).

Kullanim:
    python test_batch_checkpoint.py          # Tum testler, checkpoint'ten devam
    python test_batch_checkpoint.py --clean   # Checkpoint'i sifirla, bastan basla

Bagimlilik: Python 3.8+, concurrent.futures
"""
import sys, os, time, subprocess, ast, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Konfigurasyon ──────────────────────────────────────────────────────────
BATCH_SIZE = 10          # Kac test paralel
TIMEOUT_SEC = 30         # Her test icin max sure
CHECKPOINT_INTERVAL = 10 # Her kac batch'te bir kaydet
OUTPUT_FILE = "_test_progress.txt"
CHECKPOINT_FILE = "_test_checkpoint.json"

# ── Loglama ────────────────────────────────────────────────────────────────
_OUT = open(Path(__file__).parent / OUTPUT_FILE, 'w', encoding='utf-8')
def log(msg):
    print(msg)
    _OUT.write(msg + '\n')
    _OUT.flush()

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# ── Test dosyalarini bul ───────────────────────────────────────────────────
def bul_test_dosyalari():
    sonuc = []
    for root, dirs, files in os.walk(str(ROOT)):
        if any(x in root for x in ['venv', '__pycache__', 'skills_backup', '.ReYMeN', '.git']):
            continue
        for f in files:
            if f.endswith('.py') and ('test_' in f or '_test.py' in f):
                sonuc.append(Path(root) / f)
    return sonuc

# ── Checkpoint ─────────────────────────────────────────────────────────────
def checkpoint_oku():
    cp_path = ROOT / CHECKPOINT_FILE
    if not cp_path.exists():
        return None
    try:
        cp = json.loads(cp_path.read_text(encoding='utf-8'))
        log(f"[CHECKPOINT] Batch {cp.get('batch', '?')}, "
            f"{len(cp.get('islenen_dosyalar', []))} dosya daha once islenmis")
        return cp
    except Exception as e:
        log(f"[CHECKPOINT] Okuma hatasi (siliniyor): {e}")
        return None

def checkpoint_kaydet(batch_no, gecti_d, basarisiz_d, timeout_d, sonuclar):
    cp = {
        "batch": batch_no, "gecti": gecti_d, "basarisiz": basarisiz_d,
        "timeout": timeout_d, "islenen_dosyalar": list(sonuclar.keys()),
        "sonuclar": sonuclar, "timestamp": time.time()
    }
    (ROOT / CHECKPOINT_FILE).write_text(
        json.dumps(cp, indent=2, ensure_ascii=False), encoding='utf-8')
    log(f"[CHECKPOINT] Batch {batch_no} kaydedildi ({len(sonuclar)} dosya)")

# ── Test calistir ──────────────────────────────────────────────────────────
def run_test(tf):
    rel = str(tf.relative_to(ROOT))
    basla = time.time()
    try:
        icerik = tf.read_text(encoding='utf-8')
        if 'if __name__' in icerik:
            r = subprocess.run([sys.executable, str(tf)],
                capture_output=True, text=True, timeout=TIMEOUT_SEC, cwd=str(ROOT))
        else:
            r = subprocess.run([sys.executable, '-m', 'pytest', str(tf), '-q', '--tb=line'],
                capture_output=True, text=True, timeout=TIMEOUT_SEC, cwd=str(ROOT))
        sure = time.time() - basla
        if r.returncode == 0:
            import re
            gecen = sum(int(m.group(1)) for m in re.finditer(r'(\d+) passed', r.stdout))
            return (rel, "OK", gecen or 1, sure, "")
        else:
            return (rel, "FAIL", 0, sure, (r.stdout + r.stderr)[-200:])
    except subprocess.TimeoutExpired:
        return (rel, "TIMEOUT", 0, TIMEOUT_SEC, "")
    except Exception as e:
        return (rel, "ERROR", 0, 0, str(e)[:200])

# ── Ana akis ───────────────────────────────────────────────────────────────
def main():
    # Sifirdan basla flag
    if '--clean' in sys.argv:
        cp_path = ROOT / CHECKPOINT_FILE
        if cp_path.exists():
            cp_path.unlink()
            log("[INFO] Checkpoint silindi, bastan basliyor")

    # Test dosyalarini bul
    all_tests = bul_test_dosyalari()
    derlenebilen = [tf for tf in all_tests if ast.parse(tf.read_text(encoding='utf-8'))]
    log(f"[INFO] Toplam: {len(derlenebilen)} test dosyasi")

    # Checkpoint'ten islenmis dosyalari al
    islenen = set()
    cp = checkpoint_oku()
    if cp:
        islenen = set(cp.get("islenen_dosyalar", []))
    else:
        log("[INFO] Checkpoint yok, yeni run basliyor")

    # Kalan dosyalar
    kalan = [tf for tf in derlenebilen
             if str(tf.relative_to(ROOT)) not in islenen]
    log(f"[INFO] Atlanan: {len(islenen)}, Kalan: {len(kalan)}\n")

    if not kalan:
        log("[INFO] Hic test kalmadi, tamam.")
        return

    # Calistir
    gecti_s = gecti_d = basarisiz_d = timeout_d = 0
    tum_sonuclar = {}
    total = len(kalan)
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_start in range(0, total, BATCH_SIZE):
        batch = kalan[batch_start:batch_start + BATCH_SIZE]
        batch_no = batch_start // BATCH_SIZE + 1

        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
            futures = {ex.submit(run_test, tf): tf for tf in batch}
            for future in as_completed(futures):
                rel, durum, sayi, sure, hata = future.result()
                tum_sonuclar[rel] = durum
                if durum == "OK":
                    gecti_s += sayi; gecti_d += 1
                    log(f"  ✅ {rel} ({sayi} test, {sure:.1f}s)")
                elif durum == "FAIL":
                    basarisiz_d += 1
                    log(f"  ❌ {rel} — {hata[:120].replace(chr(10),' | ')}")
                elif durum == "TIMEOUT":
                    timeout_d += 1
                    log(f"  ⏰ {rel} (timeout)")
                else:
                    basarisiz_d += 1
                    log(f"  ❌ {rel} — {hata[:100]}")

        log(f"  --- Batch {batch_no}/{total_batches} tamam ---\n")

        if batch_no % CHECKPOINT_INTERVAL == 0:
            checkpoint_kaydet(batch_no, gecti_d, basarisiz_d, timeout_d, tum_sonuclar)

    # Final checkpoint
    checkpoint_kaydet("FINAL", gecti_d, basarisiz_d, timeout_d, tum_sonuclar)

    log(f"\n{'='*55}")
    log(f"  FINAL: {total} dosya, ✅{gecti_d} ❌{basarisiz_d} ⏰{timeout_d}")
    log(f"  BASARI: {gecti_d/total*100:.1f}%")

if __name__ == '__main__':
    main()
