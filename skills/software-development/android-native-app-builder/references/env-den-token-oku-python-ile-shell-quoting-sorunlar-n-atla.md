# .env'den token oku (Python ile, shell quoting sorunlarını atla)
with open(r'C:\Users\marko\AppData\Local\hermes\.env') as f:
    content = f.read()
match = re.search(r'^TELEGRAM_BOT_TOKEN=*** content, re.MULTILINE)
token = match.group(1).strip()
chat_id = "6328823909"  # kullanıcının chat_id'si