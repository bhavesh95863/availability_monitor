import frappe
from datetime import datetime, timedelta
from availability_monitor.utils import (
    is_host_reachable_by_ping,
    is_host_reachable_by_http,
)


def check_site_status():
    now = datetime.now()
    monitors = frappe.get_all(
        "Availability Monitor",
        fields=[
            "name",
            "ip_or_domain",
            "check_interval",
            "last_checked_at",
            "check_mode",
        ],
    )

    for monitor in monitors:
        name = monitor.name
        host = monitor.ip_or_domain
        check_mode = monitor.check_mode or "ping"
        interval = monitor.check_interval or 30
        last_checked = monitor.last_checked_at or (
            now - timedelta(minutes=interval + 1)
        )

        # Check only if interval has passed
        if (now - last_checked).total_seconds() >= interval * 60:
            is_up = False

            if check_mode == "ping":
                is_up = is_host_reachable_by_ping(host)
            elif check_mode == "http":
                is_up = is_host_reachable_by_http(host)

            frappe.db.set_value(
                "Availability Monitor",
                name,
                {
                    "status": "Online" if is_up else "Unreachable",
                    "last_checked_at": now,
                },
            )
