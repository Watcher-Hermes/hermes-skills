# TAP output for CI
prove -l --formatter TAP::Formatter::JUnit t/ > results.xml
```

### .proverc Configuration

```text
-l
--color
--timer
-r
-j4
--state=save
```