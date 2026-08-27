# Part 1 - Question 1

## Python Service Monitor

`monitor.py` checks the status of `httpd`, `rabbitMQ`, and `postgreSQL` using Linux `systemctl` and writes one JSON file per service.

## Run

```bash
python3 monitor.py
```

By default, JSON files are written to `./output/`.

To use another directory:

```bash
export RBCAPP1_STATUS_DIR=/var/log/rbcapp1
python3 monitor.py
```

## Expected JSON

Each file contains `service_name`, `service_status`, `host_name`, and `@timestamp`. The required service status values are `UP` and `DOWN`.

## Notes

The service unit names can vary slightly by Linux distribution. If PostgreSQL or RabbitMQ uses a different systemd unit on the test machine, update the `SERVICES` mapping in `monitor.py`.
