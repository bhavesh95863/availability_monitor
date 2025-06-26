## Description

**Frappe Availability Monitor** is a lightweight and flexible monitoring app for the Frappe framework that allows you to track the availability of servers, domains, and websites. Each entry can have its own check interval and method (`ping` or `http`), and the system will automatically check and update the status periodically. It also supports real-time status checks on first save and notification alerts when a monitored target goes down or comes back online.

---

## Features

- Monitor IP addresses, domains, or full URLs.
- Choose between `ping` (ICMP) or `http` (HTTPS request) check modes per entry.
- Automatically check based on a custom interval (e.g., every 30 minutes).
- Track current status: `Online` or `Unreachable`.
- Perform immediate health check on first save.
- Run background checks using Frappe's scheduler.
- Receive email or system notifications on status changes (up/down).
