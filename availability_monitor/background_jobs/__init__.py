# background_job.py

import frappe
from datetime import datetime, timedelta
from availability_monitor.utils import (
    is_host_reachable_by_ping,
    is_host_reachable_by_http,
)
from availability_monitor.availability_monitor.doctype.availability_monitor_log.availability_monitor_log import (
    create_log_entry,
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
            "retry_attempts",
            "retry_delay",
        ],
    )

    for monitor in monitors:
        name = monitor.name
        host = monitor.ip_or_domain
        check_mode = monitor.check_mode or "ping"
        interval = monitor.check_interval or 30
        retries = monitor.retry_attempts or 3
        delay = monitor.retry_delay or 2
        last_checked = monitor.last_checked_at or (
            now - timedelta(minutes=interval + 1)
        )

        if (now - last_checked).total_seconds() >= interval * 60:
            is_up = False
            response_time = 0.0
            error_message = ""
            attempt = 1

            if check_mode == "ping":
                is_up, response_time, error_message, attempt = (
                    is_host_reachable_by_ping(host, retries, delay)
                )
            elif check_mode == "http":
                is_up, response_time, error_message, attempt = (
                    is_host_reachable_by_http(host, retries, delay)
                )

            status = "Online" if is_up else "Unreachable"

            # Update main document
            frappe.db.set_value(
                "Availability Monitor",
                name,
                {
                    "status": status,
                    "last_checked_at": now,
                },
            )

            # Log this check
            create_log_entry(
                monitor_name=name,
                check_mode=check_mode,
                result=status,
                response_time=response_time,
                error_message=error_message,
                attempt_number=attempt,
            )
