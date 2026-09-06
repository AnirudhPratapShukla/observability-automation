# Part 5 - Question 5: Elastic Agent & Fleet Management

## Overview

This solution designs a Fleet-managed Elastic Agent deployment for the
rbcapp1 monitoring environment.

Fleet provides centralized management of Elastic Agents through Kibana and
allows a common monitoring policy to be assigned to multiple hosts.

## Environment

The monitoring environment contains:

| Host | IP Address |
|---|---|
| host1 | 10.0.1.10 |
| host2 | 10.0.1.11 |
| host3 | 10.0.1.12 |

## Required Data Collection

The Fleet policy is designed to collect:

- System logs from `/var/log/syslog`
- Authentication logs from `/var/log/auth.log`
- CPU metrics
- Memory metrics
- Disk metrics
- rbcapp1 application logs from `/var/log/rbcapp1/*.log`
- Monitoring information for httpd, rabbitMQ, and postgreSQL

## Files

### `fleet-agent-policy.json`

Documents the Agent Policy and required inputs, data streams, hosts, and
service monitoring configuration.

### `fleet-setup.md`

Provides step-by-step instructions for:

- Fleet Server setup
- Agent Policy creation
- System log collection
- System metrics collection
- rbcapp1 log collection
- Elastic Agent enrollment on host1, host2, and host3
- Verification and troubleshooting

### `beats-vs-fleet-comparison.md`

Compares traditional Beats deployment with Fleet-managed Elastic Agents in
terms of:

- Management
- Scalability
- Configuration
- Troubleshooting
- Operational overhead

## Verification

After implementation, verify:

1. Fleet Server is healthy.
2. host1 Elastic Agent is enrolled.
3. host2 Elastic Agent is enrolled.
4. host3 Elastic Agent is enrolled.
5. All agents are assigned the `rbcapp1-fleet-policy`.
6. System logs are being received.
7. Authentication logs are being received.
8. CPU, memory, and disk metrics are being received.
9. rbcapp1 application logs are being received.
10. Service monitoring data is available in Elasticsearch.

## Security

- Do not commit Fleet enrollment tokens.
- Do not commit API keys or passwords.
- Use TLS for production communication.
- Use least-privilege access.
- Restrict Fleet management to authorized administrators.
- Store secrets using an approved secure secret-management solution.

## Expected Result

The final Fleet deployment provides centralized monitoring and management of
the three rbcapp1 hosts while reducing the operational overhead associated
with individually managed Beats agents.
