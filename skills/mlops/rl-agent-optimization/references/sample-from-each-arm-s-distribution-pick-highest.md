# Sample from each arm's distribution, pick highest
        samples = {arm: np.random.beta(self.alpha.get(arm, 1),
                                       self.beta.get(arm, 1))
                   for arm in available_arms}
        return max(samples, key=samples.get)

    def update(self, arm, reward):