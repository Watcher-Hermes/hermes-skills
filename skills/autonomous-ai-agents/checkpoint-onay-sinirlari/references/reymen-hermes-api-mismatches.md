# Reymen ↔ Hermes API Mismatches

Bu session'da tespit edilen API farklılıkları. Reymen testleri eski
Reymen API'sine göre yazılmış, Hermes'te aynı sınıflar farklı isimlerle
veya farklı parametrelerle yer alıyor.

## Eski Reymen → Hermes Sınıf Eşlemesi

| Eski Reymen İsmi | Hermes Karşılığı | Durum |
|---|---|---|
| `ContextEngine` | `agent.context_engine.ContextEngine` | ✅ Shim çalışıyor |
| `ConversationLoop` | `agent.conversation_loop` (farklı sınıf adı) | ❌ İsim uyuşmazlığı |
| `ToolGuardrails` | `agent.tool_guardrails` (farklı sınıf adı) | ❌ İsim uyuşmazlığı |
| `MemoryManager` | `agent.memory_manager.MemoryManager` | ✅ Shim çalışıyor |
| `ChatHelper` | `agent.chat_completion_helpers` (farklı sınıf) | ❌ API farklı |
| `JsonBackend`, `SQLiteBackend` | `agent.memory_provider`'da yok | ❌ Silinmiş |
| `Display` | `agent.display` (farklı sınıf adı) | ❌ İsim uyuşmazlığı |
| `ProcessingOutcome` | Yoktu → `base.py`'ye eklendi (stub) | ✅ Eklendi |
| `MessageDeduplicator` | Yoktu → `base.py`+`helpers.py`'ye eklendi (stub) | ✅ Eklendi |
| `cache_image_from_bytes()` | Yoktu → `base.py`'ye eklendi | ✅ Eklendi |

## Test Dosyalarının Import Farkı

- **Reymen testleri** (`tests/`): root'tan import (`from context_engine import X`)
- **Hermes reference testleri** (`tests/hermes_reference/`): pytest, `agent.X`'den import
- Çözüm: Root shim (yukarıdaki pattern) + doğrudan stub ekleme
