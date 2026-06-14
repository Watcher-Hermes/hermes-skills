## How It Works

### Framework Detection

Before applying standards, determine the framework from the build file:

- Build file contains `quarkus` → apply **[QUARKUS]** conventions
- Build file contains `spring-boot` → apply **[SPRING]** conventions
- Neither detected → apply shared conventions only