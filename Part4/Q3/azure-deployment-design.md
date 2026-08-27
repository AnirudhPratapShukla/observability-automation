# Part 4 - Q3: Azure-Native ELK Deployment Design

## Overview

This document compares three deployment models for the Elastic Stack on Azure:

1. Elastic Cloud on Azure
2. Self-managed Elastic Stack on Azure Virtual Machines
3. Self-managed Elastic Stack on Azure Kubernetes Service (AKS)

The recommended option depends on the organization's operational requirements,
scalability needs, level of control, and integration requirements with Azure services.

---

## 1. Deployment Model Comparison

### 1.1 Elastic Cloud on Azure

Elastic Cloud is a managed Elastic Stack service running on Azure.

#### Management Overhead

Management overhead is low because Elastic manages most of the underlying
Elastic Stack infrastructure, including upgrades, availability and scaling
operations.

The operations team mainly focuses on configuration, data ingestion,
security, dashboards and monitoring.

#### Scalability

Elastic Cloud provides managed scaling options. Resources can be increased
based on data volume, search workload and retention requirements.

#### Azure Integration

Elastic Cloud can be deployed on Azure and can integrate with Azure-based
applications and services.

It reduces the amount of infrastructure management required by the customer.

#### Advantages

- Low infrastructure management
- Faster deployment
- Easier upgrades and maintenance
- Good scalability
- Less operational effort

#### Disadvantages

- Less infrastructure-level control
- Cost can increase with data and workload
- Some advanced infrastructure customization may not be available

---

### 1.2 Self-Managed Elastic Stack on Azure VMs

In this model, Elasticsearch, Kibana and other Elastic components are
installed and managed directly on Azure Virtual Machines.

#### Management Overhead

The operations team is responsible for:

- VM provisioning
- Operating system maintenance
- Elastic Stack installation
- Version upgrades
- Patching
- Monitoring
- Backup and recovery
- Capacity planning
- High availability configuration

#### Scalability

Scaling normally requires increasing VM resources or adding additional VMs
and Elastic nodes.

This provides good control but requires more operational work.

#### Azure Integration

The deployment can use Azure services such as:

- Azure Virtual Network
- Azure Monitor
- Azure Key Vault
- Azure Active Directory
- Azure Managed Disks
- Azure Load Balancer

#### Advantages

- Full infrastructure control
- Flexible configuration
- Ability to customize the Elastic environment
- Can use Azure infrastructure services directly

#### Disadvantages

- High operational overhead
- Manual maintenance
- More responsibility for upgrades and failures
- Capacity planning is required
- Scaling is more operationally complex

---

### 1.3 Self-Managed Elastic Stack on AKS

In this model, Elasticsearch and other Elastic components run as
containers inside Azure Kubernetes Service.

#### Management Overhead

AKS manages the Kubernetes control plane, but the organization still
manages the Elastic Stack running inside the cluster.

The team is responsible for:

- Kubernetes workloads
- Elastic configuration
- Persistent storage
- Upgrades
- Monitoring
- Security
- Networking
- Resource limits
- High availability

#### Scalability

AKS provides container and infrastructure scaling capabilities.

Elastic nodes can be distributed across Kubernetes nodes and scaled based
on workload requirements.

#### Azure Integration

AKS can integrate with:

- Azure Active Directory
- Azure Key Vault
- Azure Monitor
- Azure networking
- Azure Load Balancer
- Azure Managed Disks

#### Advantages

- Good scalability
- Container-based deployment
- Infrastructure automation
- Kubernetes orchestration
- Good integration with Azure services
- Suitable for organizations already using Kubernetes

#### Disadvantages

- Higher operational complexity
- Requires Kubernetes knowledge
- Elastic and Kubernetes both need to be managed
- Persistent storage requires careful planning
- Troubleshooting can be more complex

---

## 2. Comparison Summary

| Area | Elastic Cloud | Azure VMs | AKS |
|------|---------------|-----------|-----|
| Management | Low | High | Medium/High |
| Infrastructure Control | Low | High | High |
| Scalability | Easy | Manual/Planned | High |
| Kubernetes Knowledge | Not required | Not required | Required |
| Maintenance | Mostly managed | Customer managed | Customer managed |
| Azure Integration | Good | Very good | Very good |
| Operational Complexity | Low | High | High |
| Customization | Medium | High | High |
| Best For | Fast managed deployment | Maximum VM control | Container/Kubernetes environments |

---

## 3. When to Recommend Elastic Cloud over Self-Managed AKS

I would recommend Elastic Cloud on Azure when the organization wants to
reduce infrastructure management and focus more on observability rather
than managing the Elastic platform itself.

For example, Elastic Cloud would be a better choice when:

- The team has limited Elasticsearch administration resources.
- Fast deployment is important.
- The organization wants managed upgrades and maintenance.
- The workload can use the capabilities provided by the managed service.
- The organization wants to reduce operational overhead.
- The team does not already have strong Kubernetes expertise.

For a bank environment such as City National Bank, this can reduce the
number of infrastructure components that the observability team needs to
maintain.

Self-managed AKS would be preferred when the organization needs deeper
infrastructure control, has strong Kubernetes expertise, or requires
specific deployment and networking customization.

---

## 4. Recommended Architecture

For a self-managed Elastic deployment on AKS, the high-level architecture
would be:

```text
                         Azure
                           |
              +------------+------------+
              |                         |
        Azure Active Directory     Azure Key Vault
              |                         |
              |                  Secrets / Certificates
              |                         |
              +------------+------------+
                           |
                         AKS
                           |
                  +--------+--------+
                  |                 |
              Kibana             Ingress
                  |                 |
                  +--------+--------+
                           |
                    Elasticsearch
                    Cluster / Nodes
                           |
              +------------+------------+
              |                         |
        Elastic Agents              Logstash
              |                         |
              +------------+------------+
                           |
                    Application Logs
                    Metrics / Events
                           |
                     Azure Monitor
