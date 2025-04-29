from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def decrypt(filename, key):
    key_bytes = key.to_bytes(16, "little")

    with open(filename, "rb") as f:
        data = bytearray(f.read())

    cipher = Cipher(algorithms.AES128(key_bytes), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(data) + decryptor.finalize()

    try:
        unpadder = padding.PKCS7(128).unpadder()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted
    except ValueError:
        print("[-] Padding error: Invalid padding bytes!")
        return None

with open("recovered_key.txt") as f:
    hex_key = f.read().strip()

key = int(hex_key, 16)

decrypted_data = decrypt("data.jpg.enc", key)

if decrypted_data:
    with open("data_decrypted.jpg", "wb") as f:
        f.write(decrypted_data)

    print("[+] Decryption complete. Saved as data_decrypted.jpg")
else:
    print("[-] Decryption failed!")
