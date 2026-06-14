## Data Structure Cheat Sheet

| Use Case | Structure | Example Key |
|----------|-----------|-------------|
| Simple cache | String | `product:123` |
| User session | Hash | `session:abc` |
| Leaderboard | Sorted Set | `scores:weekly` |
| Unique visitors | Set | `visitors:2024-01-01` |
| Activity feed | List | `feed:user:456` |
| Event stream | Stream | `events:orders` |
| Counters / rate limits | String (INCR) | `ratelimit:user:123` |
| Bloom filter / HLL | HyperLogLog | `hll:pageviews` |