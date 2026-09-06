# Beats vs Fleet Comparison

## Overview

Elastic Agent with Fleet provides centralized management for the rbcapp1
monitoring environment. Traditional Beats deployments require individual
agents and configurations to be managed separately on each host.

## Management

### Traditional Beats

With Beats, each host requires individual Beat installation and configuration.

For host1, host2, and host3, administrators may need to:

- Install the appropriate Beat.
- Configure inputs.
- Configure Elasticsearch output.
- Update configuration files.
- Restart agents after configuration changes.

### Fleet

Fleet provides centralized management through Kibana.

Administrators can:

- Create a central Agent Policy.
- Assign the policy to multiple hosts.
- Update integrations centrally.
- Monitor agent health.
- Manage agent enrollment from Fleet.

**Advantage: Fleet**

## Scalability

### Traditional Beats

As the number of hosts increases, individual configuration and maintenance
becomes more difficult.

Each host may require separate configuration changes and operational checks.

### Fleet

Fleet allows a common Agent Policy to be assigned to many Elastic Agents.

For the rbcapp1 environment, the same policy can be assigned to:

```text
host1
host2
host3
