# "Kopyala" Uyarısı — VS Code'a Otomatik Gönderme YASAK

## Kural

"Kopyala", "kopyala ben yapıştırırım", "bana gönder", "gönder" dendiğinde:
- Metni HERMES CHAT'te göster
- Kullanıcı kendisi kopyalayıp yapıştırsın
- ASLA VS Code / Claude Code / herhangi bir yere otomatik gönderme

## Neden

Kullanıcı özellikle belirtti: "kesin mir culadue göndermeyeceğim" ve
"ben yapıştır a islemei yapacam sen neden yapma" — yani kullanıcı
kontrolü kendinde tutmak istiyor.

## Pitfall

"Kopyala" ile "VS Code'a yaz" KARIŞTIRILMAMALI:
- "VS Code'a yaz", "Claude terminaline yaz", "agent'a yaz" → vscode_yaz.bat
- "kopyala", "gönder", "bana gönder", "kopyala ben yapıştırırım" → burada göster
- "sana denileni yap kopyala" → yine burada göster (yönlendirme değil, sunum)

Eski emir/pattern varsa hemen sil, yoksa hata tekrarlanır.
