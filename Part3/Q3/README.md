# Part 3 - Question 3: Auto-Remediation

## Overview

This solution automatically checks the health of the rbcapp1 services using
the REST API created in Part 1 / Question 2.

If a service is detected as DOWN, the script attempts to restart the service
using the Linux `systemctl restart` command.

After the restart attempt, the script checks the service again and records the
remediation result in Elasticsearch.

## Monitored Services

The script monitors:

- httpd
- rabbitMQ
- postgreSQL

## Workflow

```text
Check REST API
      |
      v
Is service DOWN?
   /       \
 No         Yes
 |           |
 v           v
Continue   systemctl restart
             |
             v
       Check service again
             |
             v
      Log result to Elasticsearch
