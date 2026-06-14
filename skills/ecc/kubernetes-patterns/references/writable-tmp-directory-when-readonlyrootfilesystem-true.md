# Writable tmp directory when readOnlyRootFilesystem: true
          volumeMounts:
            - name: tmp
              mountPath: /tmp

      volumes:
        - name: tmp
          emptyDir: {}
```

---