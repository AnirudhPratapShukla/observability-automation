# Part 8 - Q1: Elasticsearch Audit Logging

## Overview

This section defines audit logging for the `rbcapp1` application and Elasticsearch security events.

The configuration captures authentication, authorization, and data access events and stores them in a dedicated audit-log index.

## Audit Events

The following events are configured for auditing:

- Authentication success
- Authentication failure
- Access denied
- Access granted
- Run-as granted
- Run-as denied
- Document read
- Document write
- Index template management
- ILM policy changes

## Audit Log Index

Audit logs are stored using the dedicated index pattern:

```text
audit-logs-rbcapp1*
