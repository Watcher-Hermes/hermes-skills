# GitHub Repo Değerlendirme Tercihi

Kullanıcı GitHub'dan yeni bir repo incelerken şu kural geçerlidir:

**"Biz skill almak istiyoruz, hafıza silmek değil"**

## Değerlendirme Kriterleri

Bir GitHub reposunu incelemeden/kurmadan önce şunu kontrol et:

| Tip | Örnek | Karar |
|-----|-------|-------|
| **Skill paketi** | SKILL.md dosyaları, markdown referansları, eğitim içeriği | ✅ Kurulur |
| **CLI aracı** | pip paketi, binary, daemon, npm paketi | ❌ Sadece kullanıcı açıkça isterse |
| **Memory sistemi** | Mnemosyne gibi Hermes hafızasını değiştiren | ❌ Hafıza silme riski |
| **Plugin** | Hermes plugin'i, config değişikliği gerektiren | ❌ Kullanıcıya bildir, kararını bekle |
| **MCP Server** | tools.json, config.yaml değişikliği | ❌ Kullanıcıya bildir, kararını bekle |

## Akış

1. Repoyu incele → README, SKILL.md, package.json/project files kontrol et
2. Sadece skill dosyaları mı var? → KUR
3. Sistem değiştiren bir şey mi (pip, daemon, config rewrite)? → KULLANICIYA SOR
4. "Bu repoda X var, bu Hermes'in hafızasını değiştiriyor veya sistem kuruyor. Kurulum için onaylıyor musun?" diye sor.
