# Generate multiple answers
        answers = []
        for _ in range(self.num_samples):
            result = self.qa(question=question)
            answers.append(result.answer)