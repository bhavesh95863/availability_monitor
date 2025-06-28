# Copyright (c) 2025, Bhavesh and contributors
# For license information, please see license.txt

from frappe.utils import now
import frappe
from frappe.model.document import Document


class AvailabilityMonitorLog(Document):
    pass


def create_log_entry(
    monitor_name, check_mode, result, response_time, error_message="", attempt_number=1
):
    frappe.get_doc(
        {
            "doctype": "Availability Monitor Log",
            "availability_monitor": monitor_name,
            "check_time": now(),
            "check_mode": check_mode,
            "result": result,
            "response_time": response_time,
            "error_message": error_message,
            "attempt_number": attempt_number,
        }
    ).insert(ignore_permissions=True, ignore_links=True)
