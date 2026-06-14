# Stage 3: Generate answer
        answer = self.generate_answer(context=context, question=question).answer
        return dspy.Prediction(answer=answer, context=context)