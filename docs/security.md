# Security

## Security Approach

Security is implemented at multiple layers:

```text
Internet
   |
   v
HTTPS
   |
   v
Nginx
   |
   v
API Key Authentication
   |
   v
FastAPI
   |
   v
Internal Docker Network
   |
   v
PostgreSQL
```

The system also uses EC2 security groups, environment-based configuration, restricted database exposure, and GitHub repository secrets.

## Security Risks and Mitigations

### 1. Unauthorized API Access

**Risk:** An exposed API could be called by unauthorized clients.

**Mitigation:** API-key authentication is implemented for protected API operations. Clients must provide the configured API key with requests.

The API key is not hardcoded into the application source code or committed to Git.

### 2. Unencrypted Network Traffic

**Risk:** HTTP traffic could expose API keys or application data.

**Mitigation:** The public API is served through HTTPS using Nginx and a Let's Encrypt TLS certificate.

HTTPS encrypts traffic between the client and the server.

### 3. Database Exposure

**Risk:** Exposing PostgreSQL directly to the internet could allow attackers to attempt database connections.

**Mitigation:** PostgreSQL communicates with FastAPI through the internal Docker network and does not need to be publicly accessible.

The EC2 security group should not allow public inbound access to port `5432`.

### 4. Secrets Committed to Git

**Risk:** Database credentials or API keys committed to Git could be exposed through repository history.

**Mitigation:**

- Secrets are supplied through environment variables.
- `.env` files are excluded using `.gitignore`.
- GitHub Actions deployment credentials are stored as GitHub Secrets.
- Private SSH keys are never committed to the repository.

### 5. Unrestricted Server Access

**Risk:** Open SSH access increases the attack surface of the EC2 instance.

**Mitigation:** SSH is controlled using the EC2 security group and key-based authentication.

For a production environment, SSH access should preferably be restricted to known administrative IP ranges or replaced with AWS Systems Manager.

### 6. CORS Misconfiguration

**Risk:** An overly permissive CORS configuration could allow untrusted web applications to interact with the API from browsers.

**Mitigation:** CORS is explicitly configured in the FastAPI application.

Allowed origins should be limited to trusted frontend origins in a production environment.

### 7. Direct Application Exposure

**Risk:** Exposing FastAPI directly to the internet would bypass the reverse proxy layer.

**Mitigation:** Nginx acts as the public entry point and forwards requests to the application.

The application should not require public exposure of its internal port when Nginx is handling external traffic.

## Principle of Least Privilege

The system follows least privilege where practical.

Examples:

- PostgreSQL is only required by the application.
- The application does not need public database access.
- GitHub Actions uses a dedicated deployment SSH credential.
- The deployment runs under the `ubuntu` server user.

## Security Limitations and Future Improvements

The current implementation is suitable for the assessment but is not a complete enterprise security architecture.

Future improvements could include:

- AWS Secrets Manager for application secrets.
- AWS Systems Manager instead of direct SSH.
- IAM roles with tightly scoped permissions.
- Private subnets for databases.
- AWS WAF.
- Automated vulnerability scanning.
- Secret rotation.
- Centralized security monitoring.
