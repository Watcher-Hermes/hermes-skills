# Stage 2: Retrieve context
        passages = self.retrieve(search_query).passages
        context = "\n".join(passages)