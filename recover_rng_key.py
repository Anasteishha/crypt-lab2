from mt19937_reverse import MT19937Reverse
import random

with open("sequence.txt") as f:
    outputs = [int(line.strip()) for line in f if line.strip()]

assert len(outputs) >= 624, "Потрібно щонайменше 624 виходи MT19937!"

reverser = MT19937Reverse()
recovered_rng = reverser.reverse(outputs)

key = recovered_rng.getrandbits(128)
print(f"[+] Recovered key: {key}")

key_hex = hex(key)[2:].upper()  

with open("recovered_key.txt", "w") as f:
    f.write(key_hex)

print("[+] Recovered key saved as HEX in recovered_key.txt")
