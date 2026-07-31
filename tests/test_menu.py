import base64
import time

import pytest

MENU_TITLES = {
    "debian": "LSIT - Linux System Inventory Tool",
    "freebsd": "LSIT - FreeBSD System Inventory Tool",
    "rocky": "LSIT - Rocky Linux System Inventory",
}

JSON_FIELDS = [
    "date", "machine", "ram", "cpu", "processus", "arborescence",
    "securite_ports", "securite_sudoers", "stockage", "uptime", "load_average",
]

TXT_MARKERS = [
    "Date de l'audit :",
    "La cible a été identifiée. Nom de la machine :",
    "Mémoire totale :",
    "Modèle du CPU :",
    "PROCESSUS ACTIFS",
    "ARBORESCENCE DOSSIERS",
    "AUDIT DE SÉCURITÉ",
    "Groupe Sudo :",
    "Ports ouverts :",
]


def _read_until(channel, marker: str, timeout: float = 20.0) -> str:
    channel.settimeout(1.0)
    buffer = ""
    deadline = time.monotonic() + timeout
    while marker not in buffer:
        if time.monotonic() > deadline:
            raise AssertionError(
                f"Timeout en attendant {marker!r} dans la sortie SSH. Reçu :\n{buffer}"
            )
        try:
            chunk = channel.recv(4096)
        except TimeoutError:
            continue
        if chunk:
            buffer += chunk.decode(errors="replace")
    return buffer


def _executer_python_distant(ssh_client, script: str):
    encode = base64.b64encode(script.encode("utf-8")).decode("ascii")
    cmd = f"python3 -c \"import base64; exec(base64.b64decode('{encode}').decode('utf-8'))\""
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    assert exit_code == 0, stderr.read().decode(errors="replace")


def _valider_rapport_json(ssh_client):
    script = (
        "import json\n"
        "data = json.load(open('rapport_lsit.json'))\n"
        f"champs = {JSON_FIELDS!r}\n"
        "manquants = [c for c in champs if c not in data]\n"
        "assert not manquants, f'Champs manquants : {manquants}'\n"
    )
    _executer_python_distant(ssh_client, script)


def _valider_rapport_txt(ssh_client):
    script = (
        "contenu = open('rapport_lsit.txt', encoding='utf-8').read()\n"
        f"marqueurs = {TXT_MARKERS!r}\n"
        "manquants = [m for m in marqueurs if m not in contenu]\n"
        "assert not manquants, f'Marqueurs manquants dans rapport_lsit.txt : {manquants}'\n"
    )
    _executer_python_distant(ssh_client, script)


def test_menu_txt_json_shell(vm_name, ssh_client):
    channel = ssh_client.invoke_shell(term="vt100")

    banner = _read_until(channel, "Votre choix")
    assert MENU_TITLES[vm_name] in banner

    channel.send("2\n")
    _read_until(channel, "Rapport TXT généré avec succès")
    channel.send("\n")
    _read_until(channel, "Votre choix")
    _valider_rapport_txt(ssh_client)

    channel.send("3\n")
    _read_until(channel, "Rapport JSON généré avec succès")
    channel.send("\n")
    _read_until(channel, "Votre choix")
    _valider_rapport_json(ssh_client)

    channel.send("4\n")
    _read_until(channel, "Commandes disponibles")
    channel.send("whoami\n")
    output = _read_until(channel, "vagrant")
    assert "vagrant" in output

    channel.send("exit\n")
    channel.close()
