## Optional Usage

```java
// PASS: Return Optional from find* methods
// [SPRING]
Optional<Market> market = marketRepository.findBySlug(slug);

// [QUARKUS] Panache
Optional<Market> market = Market.find("slug", slug).firstResultOptional();

// PASS: Map/flatMap instead of get()
return market
    .map(MarketResponse::from)
    .orElseThrow(() -> new EntityNotFoundException("Market not found"));
```