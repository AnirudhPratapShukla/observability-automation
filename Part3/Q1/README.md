# Part 3 - Question 1: Scheduled Service Monitoring

## Overview

This solution provides scheduled monitoring for the rbcapp1 services.

The monitoring script checks the required services and records their status.
A wrapper script is provided to run the monitoring process.

## Monitored Services

- httpd
- rabbitMQ
- postgreSQL

## Files

- `monitor.py` - Python monitoring script.
- `run_monitor.sh` - Shell wrapper used to execute the monitor.
- `logs/` - Runtime log location.
- `output/` - Generated service status output.

## Run Manually

Make the wrapper executable:

```bash
chmod +x run_monitor.sh
