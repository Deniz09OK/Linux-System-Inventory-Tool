import os
import subprocess
from pathlib import Path

import paramiko
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

VM_NAMES = ["debian", "freebsd", "rocky"]

WEB_PORTS = {"debian": 8081, "freebsd": 8082, "rocky": 8083}


@pytest.fixture(scope="session", autouse=True)
def vagrant_up():
    subprocess.run(["vagrant", "up", *VM_NAMES], cwd=REPO_ROOT, check=True)


@pytest.fixture(params=VM_NAMES)
def vm_name(request):
    return request.param


@pytest.fixture
def web_port(vm_name):
    return WEB_PORTS[vm_name]


def _parse_ssh_config(vm: str) -> dict:
    result = subprocess.run(
        ["vagrant", "ssh-config", vm],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    info = {}
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("Host "):
            continue
        key, _, value = line.partition(" ")
        info[key] = value.strip().strip('"')
    return info


@pytest.fixture
def ssh_info(vm_name):
    info = _parse_ssh_config(vm_name)
    return {
        "hostname": info["HostName"],
        "port": int(info["Port"]),
        "username": info["User"],
        "key_filename": info["IdentityFile"],
    }


@pytest.fixture
def ssh_client(ssh_info):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=ssh_info["hostname"],
        port=ssh_info["port"],
        username=ssh_info["username"],
        key_filename=ssh_info["key_filename"],
        look_for_keys=False,
        allow_agent=False,
    )
    yield client
    client.close()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    if os.environ.get("CI"):
        return browser_type_launch_args
    return {**browser_type_launch_args, "headless": False}
