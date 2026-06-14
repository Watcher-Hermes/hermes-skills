# Graceful shutdown
      terminationGracePeriodSeconds: 30

      containers:
        - name: my-app
          image: ghcr.io/org/my-app:1.0.0   # Never use :latest
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8080
              protocol: TCP