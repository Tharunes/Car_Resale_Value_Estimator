import secrets

secret_key = secrets.token_hex(16)  # 16 bytes provides a good balance of security and usability

print("Generated Secret Key:", secret_key)
