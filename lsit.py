import subprocess

with open("/etc/hostname") as f:
    hostname = f.read().strip()

print(f"La cible a été identifiée. Nom de la machine : {hostname}")

ram_info = ""
with open("/proc/meminfo") as f:
    for ligne in f:
        if "MemTotal" in ligne:
            ram_info = ligne.strip()

print(f"Mémoire totale : {ram_info}")

cpu_info = "Inconnu"
with open("/proc/cpuinfo", "r") as f:
    for ligne in f:
        if "model name" in ligne:
            cpu_info = ligne.split(":")[1].strip()
            break

cmd_ps = subprocess.run(["ps", "aux"], capture_output=True, text=True)
processus_actifs = cmd_ps.stdout

cmd_tree = subprocess.run(["tree", "-L", "2", "/home/vagrant"], capture_output=True, text=True)
arborescence = cmd_tree.stdout

with open("rapport_lsit.txt", "a") as f:
    f.write(f"La cible a été identifiée. Nom de la machine : {hostname}\n")
    f.write(f"Mémoire totale : {ram_info}\n")
    f.write(f"Modèle du CPU : {cpu_info}\n")

    f.write("\n===================================\n")
    f.write("        PROCESSUS ACTIFS           \n")
    f.write("===================================\n")
    f.write(processus_actifs)

    f.write("\n===================================\n")
    f.write("      ARBORESCENCE DOSSIERS        \n")
    f.write("===================================\n")
    f.write(arborescence)
