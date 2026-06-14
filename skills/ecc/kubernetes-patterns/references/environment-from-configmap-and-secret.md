# Environment from ConfigMap and Secret
          envFrom:
            - configMapRef:
                name: my-app-config
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: my-app-secrets
                  key: db-password