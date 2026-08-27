# Part 5 - Q1: Elasticsearch Index Template and ILM

## Overview

This section configures Elasticsearch for the RBAPP1 service status data.

The configuration includes an Index Lifecycle Management (ILM) policy and
an index template for service status documents.

## ILM Policy

Policy name:

`service-status-policy`

The policy uses the following lifecycle phases:

- Hot: rollover after 1 day
- Warm: starts after 7 days
- Delete: starts after 30 days

The policy was created using:

```bash
curl -X PUT "http://127.0.0.1:9200/_ilm/policy/service-status-policy" \
  -H "Content-Type: application/json" \
  --data-binary @ilm-policy.json
