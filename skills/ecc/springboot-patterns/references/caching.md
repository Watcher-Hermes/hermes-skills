## Caching

Requires `@EnableCaching` on a configuration class.

```java
@Service
public class MarketCacheService {
  private final MarketRepository repo;

  public MarketCacheService(MarketRepository repo) {
    this.repo = repo;
  }

  @Cacheable(value = "market", key = "#id")
  public Market getById(Long id) {
    return repo.findById(id)
        .map(Market::from)
        .orElseThrow(() -> new EntityNotFoundException("Market not found"));
  }

  @CacheEvict(value = "market", key = "#id")
  public void evict(Long id) {}
}
```