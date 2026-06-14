## Exception Mapping

```java
@Provider
public class ValidationExceptionMapper implements ExceptionMapper<ConstraintViolationException> {
  @Override
  public Response toResponse(ConstraintViolationException exception) {
    String message = exception.getConstraintViolations().stream()
        .map(cv -> cv.getPropertyPath() + ": " + cv.getMessage())
        .collect(Collectors.joining(", "));

    return Response.status(Response.Status.BAD_REQUEST)
        .entity(Map.of("error", "validation_error", "message", message))
        .build();
  }
}

@Provider
@Slf4j
public class GenericExceptionMapper implements ExceptionMapper<Exception> {

  @Override
  public Response toResponse(Exception exception) {
    log.error("Unhandled exception", exception);
    return Response.status(Response.Status.INTERNAL_SERVER_ERROR)
        .entity(Map.of("error", "internal_error", "message", "An unexpected error occurred"))
        .build();
  }
}
```