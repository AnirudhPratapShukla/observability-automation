# RBAPP1 Security & Compliance Architecture

## 1. Overview

This document defines the security and compliance architecture for the rbcapp1
ELK observability platform running on Azure Kubernetes Service (AKS).

The design addresses:

- Encryption in transit
- Encryption at rest
- Role-based access control (RBAC)
- Azure Active Directory (Microsoft Entra ID) SSO
- Data retention
- PII and PHI protection
- Audit logging
- Compliance validation
- SOC 2 Type II and HIPAA security requirements

The architecture follows least privilege, defense in depth, data minimization,
and centralized identity management principles.

No passwords, API keys, private keys, or other sensitive credentials are stored
in this repository.

---

# 2. High-Level Architecture

```text
                    Microsoft Entra ID
                           |
                      SAML SSO
                           |
                           v
                    +-------------+
                    |   Kibana    |
                    +-------------+
                           |
                       HTTPS/TLS
                           |
                           v
+-------------+     +-------------------+     +-------------+
|  rbcapp1    | --> | Elasticsearch      | --> | Azure      |
| Application |     | Cluster on AKS     |     | Monitor /  |
+-------------+     +-------------------+     | SIEM        |
       |                     ^                +-------------+
       |                     |
       v                     |
+-------------+        +------------+
| Logstash /  |------->| Audit Logs |
| Elastic     |  TLS   | 90-day ILM |
| Agent       |        +------------+
+-------------+

All production communication is encrypted using TLS.
Sensitive data is classified and protected before or during ingestion.
