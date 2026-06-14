# Take top 3
        top_passages = [p for _, p in sorted(scored, reverse=True)[:3]]
        context = "\n\n".join(top_passages)