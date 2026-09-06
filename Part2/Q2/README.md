# Part 2 - Question 2: Ansible Playbook

## Overview

This solution uses an Ansible playbook named `assignment.yml` to perform
different infrastructure and monitoring actions based on the `action`
variable.

Supported actions:

- `verify_install`
- `check-disk`
- `check-status`

## Requirements

- Ansible installed on the control machine
- SSH access to the target Linux hosts
- Inventory file from Part 2 / Question 1
- Appropriate privileges for service installation and system checks

## Inventory

The playbook uses the inventory from:

```text
../Q1/inventory
