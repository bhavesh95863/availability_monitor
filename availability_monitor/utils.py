import subprocess
import requests
import time


def is_host_reachable_by_ping(host: str, retries=3, delay=2):
    error = ""
    for attempt in range(1, retries + 1):
        start = time.time()
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "2", host],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            end = time.time()
            if result.returncode == 0:
                return True, round(end - start, 2), "", attempt
        except Exception as e:
            error = str(e)
        time.sleep(delay)
    return False, 0.0, error or "Ping failed", retries


def is_host_reachable_by_http(url: str, retries=3, delay=2):
    error = ""
    for attempt in range(1, retries + 1):
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            end = time.time()
            if response.status_code == 200:
                return True, round(end - start, 2), "", attempt
            else:
                return (
                    False,
                    round(end - start, 2),
                    f"HTTP {response.status_code}",
                    attempt,
                )
        except Exception as e:
            error = str(e)
        time.sleep(delay)
    return False, 0.0, error or "HTTP request failed", retries
