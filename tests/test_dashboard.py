import time

import pytest
from playwright.sync_api import expect

TEXT_FIELD_IDS = [
    "hostname", "cpu_info", "ram_info", "uptime", "load_average",
    "utilisateurs_sudo", "ports_ouverts", "stockage", "arborescence",
    "processus_actifs",
]


@pytest.fixture
def dashboard_running(ssh_client, web_port):
    _, stdout, _ = ssh_client.exec_command("pkill -f '[l]sit --serve'")
    stdout.channel.recv_exit_status()
    _, stdout, _ = ssh_client.exec_command("nohup lsit --serve > /tmp/lsit-serve.log 2>&1 < /dev/null & disown")
    stdout.channel.recv_exit_status()

    check = (
        "python3 -c \"import socket; s = socket.socket(); s.settimeout(1); "
        "s.connect(('127.0.0.1', 5000))\""
    )
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        _, stdout, _ = ssh_client.exec_command(check)
        if stdout.channel.recv_exit_status() == 0:
            break
        time.sleep(0.5)
    else:
        raise AssertionError(f"lsit --serve n'a jamais ouvert le port {web_port}")

    yield
    ssh_client.exec_command("pkill -f '[l]sit --serve'")


def test_dashboard_affiche_les_donnees(vm_name, web_port, dashboard_running, page):
    erreurs_console = []
    page.on(
        "console",
        lambda msg: erreurs_console.append(msg.text)
        if msg.type == "error" and "Failed to load resource" not in msg.text
        else None,
    )

    requetes_echouees = []
    page.on(
        "response",
        lambda res: requetes_echouees.append(f"{res.status} {res.url}")
        if res.status >= 400 and "favicon" not in res.url
        else None,
    )

    page.goto(f"http://127.0.0.1:{web_port}")

    expect(page).to_have_title("LSIT — Tableau de Bord")

    for field_id in TEXT_FIELD_IDS:
        locator = page.locator(f"#{field_id}")
        expect(locator).not_to_be_empty()

    expect(page.locator(".stat-label", has_text="LOAD AVERAGE")).to_be_visible()

    assert not requetes_echouees, f"Requêtes en échec : {requetes_echouees}"
    assert not erreurs_console, f"Erreurs console JS détectées : {erreurs_console}"
