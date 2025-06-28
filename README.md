# Frappe Availability Monitor

## Description

**Frappe Availability Monitor** is a lightweight and flexible monitoring app built for the Frappe framework. It enables you to track the availability of servers, domains, and websites in real-time. Each monitored target supports custom check intervals and selectable methods (`ping` or `http`). The system performs periodic checks automatically and updates the availability status. You also get instant feedback on first save and optional email notifications when a target goes down or comes back online.

---

## Features

- Monitor any IP address, domain name, or full website URL.
- Per-target configurable check mode: `ping` (ICMP) or `http` (GET request).
- Flexible check intervals (e.g., every 5, 10, 30 minutes).
- Track and update live status: `Online` or `Unreachable`.
- Real-time check and status update upon first-time creation.
- Background scheduler performs continuous checks using Frappe jobs.
- Email or in-app system notifications on status changes (Up/Down).
- Retry logic with configurable attempt count and delay.
- Logs each check with response time, result, and retry attempt info.

---

## Usage

After installing the app:

1. Create a new **Availability Monitor** entry.
2. Choose `ping` or `http` mode and set your target (IP, domain, or URL).
3. Set the desired check interval and retry options.
4. The app will begin monitoring automatically via background jobs.
5. Notifications and logs will be generated on status change.

---

## Requirements

- Frappe v14 or later
- Python 3.10+
- Redis + background workers configured for scheduled jobs

---

## Installation

```bash
bench get-app availability_monitor
bench --site [yoursite] install-app availability_monitor
