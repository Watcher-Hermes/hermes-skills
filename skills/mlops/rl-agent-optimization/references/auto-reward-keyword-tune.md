# auto_reward Keyword List Tuning — 14 June 2026

## Problem

`auto_reward()` used single-word negative keywords that matched normal conversational
speech, falsely inflating beta (failure) counts across 5 skills:

| Skill | alpha | beta | total | Status |
|-------|-------|------|-------|--------|
| adb-sdk-path-fix | 1 | 7 | 6 | Killed by false negatives |
| usb-driver-kontrol | 2 | 7 | 7 | Killed by false negatives |
| kali-linux-remote | 3 | 7 | 8 | Killed by false negatives |
| youtube-content | 1 | 7 | 6 | Killed by false negatives |
| tor-browser-arama | 13 | 7 | 18 | High usage but beta inflated |

These skills became unpickable by MAB (beta=7 means the Thompson sample is
nearly zero) — not because they performed poorly, but because common Turkish
words like "degil", "hayir", "tekrar" in the user's follow-up reply triggered -1.

## Root Cause

The old negative keyword list used single words:

- "degil" — appears in almost any negation ("o degil", "oyle degil", "bugun degil")
- "hayir" — appears in "hayirli", "hayirli olsun" (positive contexts)
- "tekrar" — appears in "tekrar dene", "tekrar yap" (action requests, not complaints)

## Fix

### 1. Single words → phrase patterns

Every keyword changed to 2-3 word phrases that genuinely signal dissatisfaction:

```
"yanlis oldu", "yanlis yaptin", "istemedigim",
"anlamadin", "duzelt bunu", "hatali calisiyor",
"olmamis bu", "calismadi", "sorun var",
"hata verdi", "bozuk bu", "yanlis anladin",
"dogru degil", "olmadi yani"
```

### 2. Positive keywords expanded

Added: "evet", "anladim", "devam", "sen karar ver", "uygula", "yap", "dene", "tmm"

"sen karar ver" and "uygula" are common user commands that signal approval
("keep going, you're doing fine"). Without these, many positive interactions
were scored neutral (reward=0).

## Validation

After fix, system continues logging (163 entries). Old entries decay via
SlidingWindowDecay (30-day half-life). MAB will gradually re-explore
the 5 killed skills as new clean data accumulates.

## Monitoring

Check every 3-5 days:

```bash
python /c/Users/marko/AppData/Local/hermes/rl_observation/rl_integration.py --action mab-data
```

Look for beta values dropping on adb-sdk-path-fix, usb-driver-kontrol,
kali-linux-remote, and youtube-content as old entries decay.

## Principle

**auto_reward is a heuristic, not ground truth.** Single-word heuristics
cannot distinguish "hayir, su degil, tekrar dene" (correction) from
"hayirli olsun, tekrar gorusuruz" (positive farewell). Phrase matching
is better but still imperfect. Periodic manual audit of MAB data health
catches drift before it corrupts 5+ arms.
