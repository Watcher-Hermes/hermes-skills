# Or use Vault
quarkus.vault.url=https://vault.example.com
quarkus.vault.authentication.kubernetes.role=my-role
```

### HashiCorp Vault Integration

```java
@ApplicationScoped
public class SecretService {

  @ConfigProperty(name = "api-key")
  String apiKey; // Fetched from Vault

  public String getSecret(String key) {
    return ConfigProvider.getConfig().getValue(key, String.class);
  }
}
```