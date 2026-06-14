# Bad: Manual loop
names = []
for user in users:
    if user.is_active:
        names.append(user.name)