# application.yml
"%dev":
  quarkus:
    datasource:
      jdbc:
        url: jdbc:postgresql://localhost:5432/dev_db
      username: dev_user
      password: ${DB_PASSWORD}
    hibernate-orm:
      database:
        generation: drop-and-create

  rabbitmq:
    host: localhost
    port: 5672
    username: ${RABBITMQ_USER}
    password: ${RABBITMQ_PASSWORD}

"%test":
  quarkus:
    datasource:
      jdbc:
        url: jdbc:h2:mem:test
    hibernate-orm:
      database:
        generation: drop-and-create

"%prod":
  quarkus:
    datasource:
      jdbc:
        url: ${DATABASE_URL}
      username: ${DB_USER}
      password: ${DB_PASSWORD}
    hibernate-orm:
      database:
        generation: validate

  rabbitmq:
    host: ${RABBITMQ_HOST}
    port: ${RABBITMQ_PORT}
    username: ${RABBITMQ_USER}
    password: ${RABBITMQ_PASSWORD}