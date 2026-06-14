# Or with specific registry
mvn package \
  -Dquarkus.container-image.build=true \
  -Dquarkus.container-image.registry=docker.io \
  -Dquarkus.container-image.group=myorg \
  -Dquarkus.container-image.tag=1.0.0