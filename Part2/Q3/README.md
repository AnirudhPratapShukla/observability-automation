# Part 2 - Question 3: Preflight Check

## Overview

`preflight_check.sh` performs preflight validation for the rbcapp1 environment
before deployment or operational activities.

The script validates connectivity and required service endpoints and reports
the results in a clear summary.

## Requirements

- Linux/Unix environment
- Bash
- Network connectivity to the target hosts
- Appropriate permissions for the checks

## Run

Make the script executable:

```bash
chmod +x preflight_check.sh
