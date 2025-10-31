# IT Policy Document

## Password Policy

### Password Requirements
- Minimum length: 12 characters
- Must contain: uppercase, lowercase, numbers, and special characters
- Cannot contain: username, company name, or common words
- Password history: Cannot reuse last 5 passwords
- Expiration: Passwords expire every 90 days

### Password Reset Procedure
1. Navigate to the IT Self-Service Portal (https://itportal.company.com)
2. Click "Forgot Password"
3. Enter your employee ID and registered email
4. Check your email for a verification code
5. Enter the code and set a new password following requirements
6. If you don't receive the email within 5 minutes, contact IT helpdesk

### Multi-Factor Authentication (MFA)
- MFA is mandatory for all employees
- Supported methods: Authenticator app (recommended), SMS, Security key
- Setup instructions available at IT portal under "Security Settings"

## VPN Access Policy

### Who Needs VPN
- All remote workers
- Employees accessing company resources from outside office
- Required for accessing internal systems, databases, and file servers

### VPN Connection Steps
1. Install company-approved VPN client (Cisco AnyConnect)
2. Launch VPN client
3. Enter VPN gateway: vpn.company.com
4. Login with company credentials + MFA
5. Connection established notification will appear

### VPN Troubleshooting
- **Cannot connect**: Check internet connection, verify credentials, ensure MFA device is accessible
- **Slow connection**: Disconnect and reconnect, try different VPN server
- **Authentication fails**: Reset password, verify MFA is working

## Email Policy

### Email Usage Guidelines
- Use company email for business purposes only
- Maximum attachment size: 25MB
- Do not share sensitive information without encryption
- Report suspicious emails to security@company.com

### Email Quota and Retention
- Mailbox quota: 50GB per user
- Emails older than 2 years are archived
- Deleted items purged after 30 days

## Software Installation Policy

### Approved Software
- Employees can install pre-approved software from Software Center
- Software requests must be submitted via IT portal
- Approval required from department head for specialized software
- Approval time: 2-3 business days

### Prohibited Software
- P2P file sharing applications
- Unauthorized cloud storage services
- Software with known security vulnerabilities
- Cracked or pirated software

## Device Management

### Laptop and Desktop Standards
- All company devices must have:
  - Updated antivirus software (automatic updates enabled)
  - Disk encryption enabled (BitLocker/FileVault)
  - Firewall enabled
  - Automatic OS updates enabled

### Mobile Device Policy
- BYOD (Bring Your Own Device) allowed with Mobile Device Management (MDM)
- Company apps must be installed through MDM
- Remote wipe capability must be enabled
- Devices must have passcode/biometric lock

## Network Access

### WiFi Access
- Office WiFi: Connect to "CompanySecure" network
- Guest WiFi: "CompanyGuest" (limited access)
- Credentials: Use company login for CompanySecure
- Guest access: Request temporary password from reception

### Network Drive Mapping
- Windows: Map network drive using \\\\fileserver.company.com\\[department]
- Mac: Connect to server: smb://fileserver.company.com/[department]
- Credentials: Use company domain credentials

## Data Security

### Data Classification
- **Public**: Can be shared freely
- **Internal**: Company employees only
- **Confidential**: Restricted access, NDA required
- **Restricted**: Executive level and authorized personnel only

### Data Handling Guidelines
- Encrypt confidential data before transmission
- Use secure file transfer methods (SFTP, encrypted email)
- Do not store sensitive data on personal devices
- Report data breaches immediately to security team

## Incident Reporting

### Security Incidents
- Report immediately to: security@company.com or call ext. 911
- Include: Time, type of incident, systems affected, actions taken

### Data Loss
- Contact IT immediately
- Do not attempt recovery yourself
- Provide details: what was lost, when, where stored

## Compliance

### Regular Requirements
- Annual security awareness training (mandatory)
- Quarterly policy review acknowledgment
- Monthly security updates reading
- Immediate reporting of policy violations

### Consequences of Policy Violations
- First offense: Warning and mandatory retraining
- Second offense: Temporary suspension of access
- Third offense: Employment review

## Contact Information

### IT Helpdesk
- Email: helpdesk@company.com
- Phone: ext. 1234 or +66-2-XXX-XXXX
- Hours: Mon-Fri 8:00-18:00
- Emergency: 24/7 hotline +66-XX-XXX-XXXX

### IT Self-Service Portal
- URL: https://itportal.company.com
- Available 24/7 for password resets, software requests, knowledge base

---
*Last Updated: October 2025*
*Version: 3.2*

