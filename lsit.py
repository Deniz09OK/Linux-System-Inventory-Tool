with open("/etc/hostname") as f:
    hostname = f.read().strip()

print(f"La cible a été identifiée. Nom de la machine : {hostname}")

ram_info = ""
with open("/proc/meminfo") as f:
    for ligne in f:
        if "MemTotal" in ligne:
            ram_info = ligne.strip()

print(f"Mémoire totale : {ram_info}")

with open("rapport_lsit.txt", "a") as rapport:
    rapport.write(f"La cible a été identifiée. Nom de la machine : {hostname}\n")
    rapport.write(f"Mémoire totale : {ram_info}\n")
