import subprocess
import requests


def is_host_reachable_by_ping(host: str) -> bool:
    try:
        output = subprocess.run(
            ["ping", "-c", "1", "-W", "2", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output.returncode == 0
    except Exception:
        return False


def is_host_reachable_by_http(host: str) -> bool:
    try:
        response = requests.get(host, timeout=5)
        return response.status_code == 200
    except Exception:
        return False
