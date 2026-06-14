## How It Works

- Structure the app around clear boundaries (controllers -> services/actions -> models).
- Use explicit bindings and scoped bindings to keep routing predictable; still enforce authorization for access control.
- Favor typed models, casts, and scopes to keep domain logic consistent.
- Keep IO-heavy work in queues and cache expensive reads.
- Centralize config in `config/*` and keep environments explicit.