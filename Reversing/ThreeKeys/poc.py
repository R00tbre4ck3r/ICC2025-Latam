#!/usr/bin/env python3

from Crypto.Cipher import AES

def main():
    print("=" * 60)
    print("    THREEKEYS CTF FLAG EXTRACTOR")
    print("=" * 60)
    
    print("[*] Extrayendo datos del binario...")
    
    key1 = bytes.fromhex("f2e7bfd753c64b2697f96987e68428e8")
    key2 = bytes.fromhex("dcf99026922733672408c64551c73a33")
    key3 = bytes.fromhex("ee31ced8107040a0d953cf57327973d5")
    
    ct_block1 = bytes.fromhex("8cebc865434846a69805e8422f3f809f")
    ct_block2 = bytes.fromhex("a8c9b37d281ad83eaaba1a2be98fb76c")
    
    print(f"[*] KEY1: {key1.hex()}")
    print(f"[*] KEY2: {key2.hex()}")
    print(f"[*] KEY3: {key3.hex()}")
    print(f"[*] CT Bloque 1: {ct_block1.hex()}")
    print(f"[*] CT Bloque 2: {ct_block2.hex()}")
    
    print("\n[*] Iniciando proceso de descifrado...")
    print("[*] Orden de descifrado: KEY3 -> KEY2 -> KEY1")
    
    print("\n[*] Descifrando bloque 1...")
    result1 = ct_block1
    result1 = AES.new(key3, AES.MODE_ECB).decrypt(result1)
    result1 = AES.new(key2, AES.MODE_ECB).decrypt(result1)
    result1 = AES.new(key1, AES.MODE_ECB).decrypt(result1)
    
    print("[*] Descifrando bloque 2...")
    result2 = ct_block2
    result2 = AES.new(key3, AES.MODE_ECB).decrypt(result2)
    result2 = AES.new(key2, AES.MODE_ECB).decrypt(result2)
    result2 = AES.new(key1, AES.MODE_ECB).decrypt(result2)
    
    full_result = result1 + result2
    flag = full_result.rstrip(b'\x08').decode('utf-8')
    
    print("\n" + "=" * 60)
    print(f"    FLAG ENCONTRADA: {flag}")
    print("=" * 60)
    
    if flag.startswith('HTB{') and flag.endswith('}'):
        print("[✓] Flag válida!")
        return flag
    else:
        print("[!] La flag podría estar incompleta o incorrecta")
        return None

if __name__ == "__main__":
    flag = main()
    if flag:
        print(f"\n[*] Para usar la flag: {flag}")
