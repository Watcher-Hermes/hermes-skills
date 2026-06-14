# BAD: Storing plaintext secrets in ConfigMaps
apiVersion: v1
kind: ConfigMap
data:
  DB_PASSWORD: "mysecretpassword"   # NEVER — use Secret or external secrets manager