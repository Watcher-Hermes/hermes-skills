# -*- coding: utf-8 -*-
"""test_batch_10.py — Testleri 10'ar 10'ar paralel calistir.
v2.1: Checkpoint sistemi — her 10 batch'te durum kaydeder, restart'ta kaldigi yerden devam eder."""
import sys, os, time, subprocess, ast, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_OUT_FILE = open(Path(__file__).parent / "_test_progress.txt", 'w', encoding='utf-8')
_CHECKPOINT = Path(__file__).parent / "_test_checkpoint.json"
def log(msg):
    print(msg)
    _OUT_FILE.write(msg + '\n')
    _OUT_FILE.flush()

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
CHECKPOINT_INTERVAL = 10

all_tests = []
for root, dirs, files in os.walk(str(ROOT)):
    if any(x in root for x in ['venv', '__pycache__', 'skills_backup', '.ReYMeN']):
        continue
    for f in files:
        if f.endswith('.py') and ('test_' in f or '_test.py' in f):
            all_tests.append(Path(root) / f)

derlenebilen = [tf for tf in all_tests if ast.parse(tf.read_text(encoding='utf-8'))]

islenen = set()
if _CHECKPOINT.exists():
    try:
        cp = json.loads(_CHECKPOINT.read_text(encoding='utf-8'))
        islenen = set(cp.get("islenen_dosyalar", []))
        log(f"[CHECKPOINT] Batch {cp.get('batch','?')}'den devam, {len(islenen)} dosya islenmis")
    except:
        pass

kalan = [tf for tf in derlenebilen if str(tf.relative_to(ROOT)) not in islenen]
log(f"[INFO] Toplam: {len(derlenebilen)}, kalan: {len(kalan)}")

def run_test(tf):
    rel = str(tf.relative_to(ROOT))
    basla = time.time()
    try:
        icerik = tf.read_text(encoding='utf-8')
        if 'if __name__' in icerik:
            r = subprocess.run([sys.executable, str(tf)], capture_output=True, text=True, timeout=30, cwd=str(ROOT))
        else:
            r = subprocess.run([sys.executable, '-m', 'pytest', str(tf), '-q', '--tb=line'], capture_output=True, text=True, timeout=30, cwd=str(ROOT))
        sure = time.time() - basla
        if r.returncode == 0:
            import re
            gecen_sayisi = sum(int(m.group(1)) for m in re.finditer(r'(\d+) passed', r.stdout))
            return (rel, "OK", max(gecen_sayisi, 1), sure, "")
        else:
            return (rel, "FAIL", 0, sure, (r.stdout + r.stderr)[-200:])
    except subprocess.TimeoutExpired:
        return (rel, "TIMEOUT", 0, 30, "")
    except Exception as e:
        return (rel, "ERROR", 0, 0, str(e)[:200])

BATCH_SIZE = 10
gecti_sayisi, gecti_dosya, basarisiz, zaman_asimi = 0, 0, 0, 0
tum_sonuclar = {}
total = len(kalan)

for batch_start in range(0, total, BATCH_SIZE):
    batch = kalan[batch_start:batch_start + BATCH_SIZE]
    batch_no = batch_start // BATCH_SIZE + 1
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
        futures = {executor.submit(run_test, tf): tf for tf in batch}
        for future in as_completed(futures):
            rel, durum, sayi, sure, hata = future.result()
            tum_sonuclar[rel] = durum
            if durum == "OK":
                gecti_sayisi += sayi; gecti_dosya += 1
                log(f"  ✅ {rel} ({sayi} test, {sure:.1f}s)")
            elif durum == "FAIL":
                basarisiz += 1
                log(f"  ❌ {rel} — {hata[:120].replace(chr(10),' | ')}")
            elif durum == "TIMEOUT":
                zaman_asimi += 1
                log(f"  ⏰ {rel} (timeout)")
            else:
                basarisiz += 1
                log(f"  ❌ {rel} — {hata[:100]}")
    log(f"  --- Batch {batch_no}/{total_batches} tamam ---\n")
    if batch_no % CHECKPOINT_INTERVAL == 0:
        _CHECKPOINT.write_text(json.dumps({"batch": batch_no, "gecti": gecti_dosya, "basarisiz": basarisiz, "timeout": zaman_asimi, "islenen_dosyalar": list(tum_sonuclar.keys()), "sonuclar": tum_sonuclar, "timestamp": time.time()}, indent=2, ensure_ascii=False), encoding='utf-8')
        log(f"[CHECKPOINT] Batch {batch_no} kaydedildi ({len(tum_sonuclar)} dosya)")

_CHECKPOINT.write_text(json.dumps({"batch": "FINAL", "gecti": gecti_dosya, "basarisiz": basarisiz, "timeout": zaman_asimi, "islenen_dosyalar": list(tum_sonuclar.keys()), "sonuclar": tum_sonuclar, "timestamp": time.time()}, indent=2, ensure_ascii=False), encoding='utf-8')
log(f"\nFINAL: {gecti_dosya} gecti, {basarisiz} basarisiz, {zaman_asimi} timeout")
