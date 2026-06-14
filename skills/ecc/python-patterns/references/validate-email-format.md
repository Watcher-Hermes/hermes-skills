# Validate email format
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")