# BAD: ClusterAdmin for application service accounts
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
roleRef:
  kind: ClusterRole
  name: cluster-admin    # Grants god-mode to your app