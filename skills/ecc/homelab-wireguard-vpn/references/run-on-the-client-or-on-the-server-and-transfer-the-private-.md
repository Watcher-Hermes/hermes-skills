# Run on the client, or on the server and transfer the private key securely — never in plaintext
umask 077
wg genkey | tee phone_private.key | wg pubkey > phone_public.key