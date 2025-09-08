

import sys

KEY_LEN = 5
KNOWN_PREFIX = b"HTB{"

def read_ciphertext(path: str) -> bytes:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read().strip()
    
    return bytes.fromhex(data)

def is_printable_ascii(bs: bytes) -> bool:
    return all(32 <= b <= 126 for b in bs)  # solo ASCII imprimible (sin control chars)

def derive_key(cipher: bytes, prefix: bytes = KNOWN_PREFIX, keylen: int = KEY_LEN) -> bytes:
    """
    Deriva los primeros 'keylen' bytes del keystream asumiendo:
      - prefijo conocido al inicio (p.ej. b'HTB{')
      - longitud de clave conocida (5)
    Obtiene K[0..3] por known-plaintext y encuentra K[4] por prueba y descarte
    (ASCII imprimible) + validación de que el texto descifrado termine en '}'.
    """
    if len(cipher) < len(prefix):
        raise ValueError("Ciphertext demasiado corto para aplicar known-plaintext.")

    K = [0] * keylen

    for i in range(len(prefix)):    
        K[i] = cipher[i] ^ prefix[i]

    # Probar candidatos para K[4]
    candidates = []
    for k4 in range(256):
        ok = True
      
        for i in range(4, len(cipher), keylen):
            p = cipher[i] ^ k4
            if not (32 <= p <= 126):
                ok = False
                break
        if ok:
            candidates.append(k4)


    for k4 in candidates:
        Ktmp = K[:]
        Ktmp[4] = k4
        pt = bytes(c ^ Ktmp[i % keylen] for i, c in enumerate(cipher))
        try:
            s = pt.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            continue
        if s.startswith("HTB{") and s.rstrip().endswith("}") and is_printable_ascii(pt):
            return bytes(Ktmp)

    raise ValueError("No se pudo inferir K[4] con las restricciones dadas.")

def decrypt(cipher: bytes, key: bytes) -> bytes:
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(cipher))

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "encrypted.txt"
    C = read_ciphertext(path)
    K = derive_key(C, KNOWN_PREFIX, KEY_LEN)
    P = decrypt(C, K)

    print("Key (hex):", K.hex())
    print("Flag:", P.decode("utf-8"))

if __name__ == "__main__":
    main()
