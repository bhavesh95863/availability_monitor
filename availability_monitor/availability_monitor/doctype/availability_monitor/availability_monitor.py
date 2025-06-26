# Copyright (c) 2025, Bhavesh and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from datetime import datetime
from availability_monitor.utils import (
    is_host_reachable_by_ping,
    is_host_reachable_by_http,
)


class AvailabilityMonitor(Document):
    def validate(self):
        # Validate input format based on check_mode
        if self.check_mode == "ping":
            if "http://" in self.ip_or_domain or "https://" in self.ip_or_domain:
                frappe.throw(
                    "For 'Ping' mode, please enter only the domain or IP without http/https."
                )
        elif self.check_mode == "http":
            if not (
                self.ip_or_domain.startswith("http://")
                or self.ip_or_domain.startswith("https://")
            ):
                frappe.throw(
                    "For 'HTTP' mode, please enter a full URL with http:// or https://."
                )

        # Set initial status on first save
        if self.is_new():
            self.status = "Online" if self.check_site_status() else "Unreachable"
            self.last_checked_at = datetime.now()

    def check_site_status(self):
        if self.check_mode == "ping":
            return is_host_reachable_by_ping(self.ip_or_domain)
        elif self.check_mode == "http":
            return is_host_reachable_by_http(self.ip_or_domain)
        return False
