## Model Swapping

LM Studio serves ONE model at a time via the API. To swap:

1. **Unload current:**
   ```bash
   lms unload <identifier>
   ```
2. **Load new (simple — auto-detects settings for small models ≤8B):**
   ```bash
   lms load <model-key> -y
   ```
   Small models (4-8GB) load in ~10s with auto-detected GPU offload. No `--gpu` or `--identifier` flags needed.

3. **Load new (with GPU offload for 14B+ models):**
   ```bash
   lms load <new-model-key> --gpu <ratio> -y --identifier <name>
   ```

4. **Restart server (REQUIRED — `lms load` does NOT start/restart the API server):**
   ```bash
   lms server start --port 1234
   ```

5. **Verify:**
   ```bash
   lms ps --json
   ```

### Server endpoint after restart

After LM Studio process kill + restart, the auto-detected IP (e.g. `169.254.250.216`) becomes stale. Always use `localhost:1234` after a restart.

---