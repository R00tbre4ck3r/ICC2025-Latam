#!/usr/bin/env python3

# Decryption key from the binary (little endian)
key_part1 = 0xc3e2af1e8edad4c6
key_part2 = 0xee602548c0d4060c

# Convert to bytes (little endian)
key = key_part1.to_bytes(8, 'little') + key_part2.to_bytes(8, 'little')
print(f"Key: {key.hex()}")

# Encrypted data for memory 3 (from address 0x2128)
encrypted_data = bytes.fromhex("8e8098f52ec1d19c7837b9f31755548a99a0adbe41dbd3ae3f59a4f42c7a1486b4e7e9d16a9e8ff05376e0a4660b4e93")

print(f"Encrypted data: {encrypted_data.hex()}")
print(f"Length: {len(encrypted_data)} bytes")

# Decrypt by XORing with the key
decrypted = bytearray()
for i, byte in enumerate(encrypted_data):
    key_byte = key[i % len(key)]
    decrypted_byte = byte ^ key_byte
    decrypted.append(decrypted_byte)

# Convert to string and print
try:
    decrypted_text = decrypted.decode('ascii')
    print(f"\nDecrypted message:")
    print(decrypted_text)
except UnicodeDecodeError:
    print(f"\nDecrypted bytes (hex): {decrypted.hex()}")
    print(f"Decrypted bytes (raw): {decrypted}")
