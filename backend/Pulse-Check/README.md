# Pulse-Check-API ("Watchdog" Sentinel)

Pulse-Check-API is a simple backend monitoring system built with Django and Django REST Framework.  
It acts like a **Dead Man’s Switch** for remote devices: each device must send heartbeats on time, otherwise the system marks it as **down** and triggers an 
alert.

This project was built to demonstrate:
- backend API design,
- stateful timer logic,
- failure detection,
- pause/snooze behavior,
- and clean documentation.

---

## Architecture Diagram

```mermaid
sequenceDiagram
    participant Device
    participant API as Pulse-Check API
    participant DB as Database

    Device->>API: POST /monitors (register device)
    API->>DB: Save monitor (timeout, alert_email, status=up)

    Device->>API: POST /monitors/{id}/heartbeat
    API->>DB: Update last_heartbeat and set status=up

    Device->>API: POST /monitors/{id}/pause
    API->>DB: Set is_paused=true

    Note over API,DB: System status check happens when /monitors/check-status/ is called

    API->>DB: Fetch all monitors
    API->>API: Compare current time with last_heartbeat

    alt Timeout exceeded and monitor not paused
        API->>DB: Update status=down
        API->>API: Console log alert JSON
    else Monitor is healthy or paused
        API->>DB: Keep status unchanged
    end
````

---

## Overview

Devices are registered with a timeout value.
When a device sends a heartbeat, the system updates the last heartbeat time and keeps the monitor active.

If too much time passes without a heartbeat, the system:

* marks the device as `down`,
* and prints an alert in the console.

This project is designed as a beginner-friendly Django backend that focuses on clear logic and clean state handling.

---

## Features

* Register a new monitor
* Receive heartbeats
* Detect timeout failures
* Mark devices as `down`
* Pause monitoring to prevent false alerts
* List all monitors for observability
* Console-based alert logging for failure simulation

---

## Tech Stack

* Python
* Django
* Django REST Framework
* SQLite

---

## Setup Instructions

### 1. Clone the repository

Clone your forked repository, not the original challenge repository.

```bash
git clone https://github.com/Hugues6221394/AmaliTech-DEG-Project-based-challenges.git
cd AmaliTech-DEG-Project-based-challenges/backend/Pulse-Check
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The server should run at:

```text
http://127.0.0.1:8000/
```

---

## API Documentation

### 1. Register a monitor

**Endpoint:**
`POST /monitors/`

**Purpose:**
Creates a new monitor for a device.

**Request Body Example:**

```json
{
  "device_id": "device-123",
  "timeout": 60,
  "alert_email": "admin@critmon.com"
}
```

**Response:**

* `201 Created` when the monitor is created successfully

---

### 2. List all monitors

**Endpoint:**
`GET /monitors/`

**Purpose:**
Returns all registered monitors.
This was added as the developer’s choice feature to improve observability.

**Response:**

* `200 OK`

**Example Response:**

```json
[
  {
    "id": 1,
    "device_id": "device-123",
    "timeout": 60,
    "alert_email": "admin@critmon.com",
    "status": "up",
    "last_heartbeat": "2026-04-29T16:00:00Z",
    "is_paused": false,
    "created_at": "2026-04-29T15:59:00Z",
    "updated_at": "2026-04-29T16:00:00Z"
  }
]
```

---

### 3. Send heartbeat

**Endpoint:**
`POST /monitors/{device_id}/heartbeat/`

**Purpose:**
Resets the countdown timer and marks the monitor as active.

**Example:**
`POST /monitors/device-123/heartbeat/`

**Behavior:**

* updates `last_heartbeat`
* sets `status = "up"`
* automatically unpauses the monitor if it was paused

**Response:**

* `200 OK` if the monitor exists
* `404 Not Found` if the monitor does not exist

---

### 4. Pause monitoring

**Endpoint:**
`POST /monitors/{device_id}/pause/`

**Purpose:**
Temporarily pauses monitoring for a device.

**Example:**
`POST /monitors/device-123/pause/`

**Behavior:**

* sets `is_paused = true`
* pauses failure detection for that device

**Response:**

* `200 OK` if the monitor exists
* `404 Not Found` if the monitor does not exist

---

### 5. Check system status

**Endpoint:**
`GET /monitors/check-status/`

**Purpose:**
Checks all monitors and determines whether any device has timed out.

**Behavior:**

* compares current time with `last_heartbeat`
* ignores paused monitors
* marks overdue monitors as `down`
* prints an alert to the console in JSON format

**Alert Example:**

```json
{
  "ALERT": "Device device-123 is down!",
  "time": "2026-04-29T16:05:00Z"
}
```

**Response:**

* `200 OK`

---

## Design Decisions

### 1. Why Django and DRF?

Django gives a clean structure for backend development, while Django REST Framework makes it easy to build JSON APIs.

### 2. Why store monitor state in the database?

This makes the application state persistent and easy to inspect.
The app can track:

* timeout,
* last heartbeat,
* pause status,
* and device status.

### 3. Why use a manual `/check-status/` endpoint?

This keeps the project simple and beginner-friendly.
In a production system, this kind of logic would usually run in a background worker or scheduled job.

### 4. Why console logging for alerts?

The challenge allows alert simulation through console logging.
This keeps the implementation simple while still showing the correct system behavior.

---

## Developer’s Choice Feature

### Monitor Listing Endpoint

I added `GET /monitors/` to improve observability.

This helps administrators:

* see all registered devices,
* check which devices are `up` or `down`,
* inspect `last_heartbeat`,
* and review whether a device is paused.

This feature was added because real monitoring systems need visibility, not only alerting.
Being able to inspect the current state of all devices makes the system more useful and easier to debug.

---

## Example Usage Flow

1. Register a monitor with `POST /monitors/`
2. Send heartbeats with `POST /monitors/{device_id}/heartbeat/`
3. Pause a monitor with `POST /monitors/{device_id}/pause/`
4. Run the system check with `GET /monitors/check-status/`
5. View all monitors with `GET /monitors/`

---

## Future Improvements

* Automatic background scheduler for timeout checks
* Email or webhook alerts instead of console logs
* Authentication and authorization
* Admin dashboard for monitor visibility
* Better concurrency handling for large-scale deployments

---

## Conclusion

Pulse-Check-API demonstrates how a backend system can manage stateful timers, detect failures, and provide real-time monitoring behavior using Django.

It was built to be simple, readable, and strong enough to show practical backend engineering thinking.

---


