# Copyright (c) 2025, Bhavesh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from availability_monitor.utils import (
    is_host_reachable_by_ping,
    is_host_reachable_by_http,
)
from frappe.utils import cint
from availability_monitor.availability_monitor.doctype.availability_monitor_log.availability_monitor_log import (
    create_log_entry,
)


import frappe
from frappe.model.document import Document
from datetime import datetime
from availability_monitor.utils import (
    is_host_reachable_by_ping,
    is_host_reachable_by_http,
)
from availability_monitor.availability_monitor.doctype.availability_monitor_log.availability_monitor_log import (
    create_log_entry,
)


class AvailabilityMonitor(Document):
    def validate(self):
        # Validate input format based on check_mode
        if self.check_mode == "ping":
            if "http://" in self.ip_or_domain or "https://" in self.ip_or_domain:
                frappe.throw(
                    "For 'Ping' mode, enter only the domain or IP without http/https."
                )
        elif self.check_mode == "http":
            if not (
                self.ip_or_domain.startswith("http://")
                or self.ip_or_domain.startswith("https://")
            ):
                frappe.throw(
                    "For 'HTTP' mode, enter a full URL with http:// or https://."
                )

        # Validate retry limits
        if self.retry_attempts and cint(self.retry_attempts) > 5:
            frappe.throw("Retry attempts should not exceed 5.")

        if self.is_new():
            is_up, response_time, error_msg, attempt = self.check_site_status(
                retries=cint(self.retry_attempts or 3),
                delay=cint(self.retry_delay or 2),
            )
            self.status = "Online" if is_up else "Unreachable"
            self.last_checked_at = datetime.now()

            create_log_entry(
                monitor_name=self.name,
                check_mode=self.check_mode,
                result=self.status,
                response_time=response_time,
                error_message=error_msg,
                attempt_number=attempt,
            )

    def check_site_status(self, retries=3, delay=2):
        if self.check_mode == "ping":
            return is_host_reachable_by_ping(self.ip_or_domain, retries, delay)
        elif self.check_mode == "http":
            return is_host_reachable_by_http(self.ip_or_domain, retries, delay)
        return False, 0.0, "Invalid check_mode", 1
