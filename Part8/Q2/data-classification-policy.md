# Data Classification and PII/PHI Handling Policy

## 1. Purpose

This policy defines how data stored and processed by the RBAPP1 Elasticsearch and Kibana environment should be classified and protected.

The policy focuses on protecting sensitive information, including Personally Identifiable Information (PII) and Protected Health Information (PHI), while maintaining the observability required for application and security monitoring.

---

## 2. Data Classification

RBAPP1 observability data is classified into the following levels.

| Classification | Description | Examples |
|---|---|---|
| Public | Information that can be shared publicly | Public documentation, application status information |
| Internal | Information intended for internal operational use | Application logs, service health information |
| Confidential | Sensitive business or operational information | Internal identifiers, system details, operational events |
| Restricted | Highly sensitive information requiring strict access control | PII, PHI, authentication information, sensitive audit data |

Restricted data must have the strongest access controls and should only be accessible to authorized personnel.

---

## 3. PII Identification

Potential PII fields in application logs should be identified during log collection and processing.

Examples include:

- Full name
- Email address
- Phone number
- Postal address
- Customer or employee identifiers
- Government identification numbers
- IP addresses where treated as personal information by applicable policy
- Authentication or session identifiers

Application teams should review log fields before sending application data to Elasticsearch.

---

## 4. PHI Identification

Where applications process healthcare-related information, PHI fields must be identified before ingestion.

Examples may include:

- Patient name
- Patient identifier
- Medical record number
- Health information
- Diagnosis information
- Treatment information
- Insurance information

PHI should not be stored in observability indices unless there is a documented business and compliance requirement.

---

## 5. PII/PHI Handling

Sensitive fields should be handled using one or more of the following methods:

### Masking

Replace sensitive values with a masked representation.

Example:

```text
john.smith@example.com
