## Pagination and Sorting

```java
PageRequest page = PageRequest.of(pageNumber, pageSize, Sort.by("createdAt").descending());
Page<Market> results = marketService.list(page);
```