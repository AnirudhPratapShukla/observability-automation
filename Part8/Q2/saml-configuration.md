# Microsoft Entra ID SAML SSO Configuration

## 1. Objective

Configure Microsoft Entra ID (formerly Azure Active Directory) as the SAML Identity Provider (IdP) for Kibana and Elasticsearch.

The objective is to provide centralized authentication through Microsoft Entra ID and use SAML attributes/groups to control Elasticsearch and Kibana access through RBAC.

No passwords, client secrets, certificates, or other sensitive credentials are stored in this repository.

---

## 2. Prerequisites

- Elasticsearch and Kibana with security enabled.
- A Microsoft Entra ID tenant.
- Administrator access to Microsoft Entra Enterprise Applications.
- Kibana must be accessible through HTTPS in production.
- A DNS name for the Kibana endpoint.
- SAML signing certificate/metadata from Microsoft Entra ID.
- Elasticsearch SAML realm configured before enabling SAML authentication.

A Microsoft Entra Cloud Application Administrator or Application Administrator role is required to manage enterprise applications.

---

## 3. Create the Microsoft Entra Enterprise Application

1. Sign in to the Microsoft Entra admin center.
2. Navigate to:

   `Entra ID -> Enterprise applications -> New application`

3. Select:

   `Create your own application`

4. Provide a name such as:

   `RBAPP1 Elasticsearch Kibana`

5. Select:

   `Integrate any other application you don't find in the gallery`

6. Create the application.

7. Open the new enterprise application.

8. Navigate to:

   `Users and groups`

9. Assign only the required users and groups.

Microsoft Entra allows application access to be restricted to assigned users and groups.

---

## 4. Configure SAML

Inside the enterprise application:

1. Open:

   `Single sign-on`

2. Select:

   `SAML`

3. Edit the **Basic SAML Configuration**.

Use the following values as environment-specific examples:

### Identifier (Entity ID)

```text
https://<KIBANA_HOST>
