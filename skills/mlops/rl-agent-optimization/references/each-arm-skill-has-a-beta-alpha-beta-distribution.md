# Each arm (skill) has a Beta(alpha, beta) distribution
        self.alpha = {}  # success count
        self.beta = {}   # failure count

    def select_arm(self, available_arms):