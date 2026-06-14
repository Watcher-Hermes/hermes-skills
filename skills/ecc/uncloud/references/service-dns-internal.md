## Service DNS (Internal)

Services inside the cluster resolve each other by name:

| DNS name | Resolves to |
|----------|------------|
| `service-name` | Any healthy container |
| `service-name.internal` | Same |
| `rr.service-name.internal` | Round-robin |
| `nearest.service-name.internal` | Machine-local first |

---