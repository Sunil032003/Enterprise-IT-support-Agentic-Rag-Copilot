# IT SERVICE DESK RUNBOOK

**Document ID:** IT-RUNBOOK-001  
**Version:** 1.0  
**Department:** IT Service Desk  
**Status:** Active  
**Document Type:** Operational Runbook  
**Last Updated:** 2026-10-11

---

## 1. Purpose

This runbook provides standardized procedures for the IT Service Desk to handle common employee IT incidents and service requests.

The objective is to:

- Resolve common IT issues quickly.
- Provide consistent troubleshooting procedures.
- Define when incidents must be escalated.
- Maintain proper incident documentation.
- Protect company systems and employee data.
- Ensure critical incidents are handled according to priority.

---

# 2. Service Desk Responsibilities

The IT Service Desk is responsible for:

1. Receiving employee IT incidents and service requests.
2. Creating and updating support tickets.
3. Categorizing and prioritizing incidents.
4. Performing first-level troubleshooting.
5. Providing approved solutions.
6. Escalating unresolved issues to appropriate teams.
7. Communicating incident status to employees.
8. Recording troubleshooting steps and resolutions.
9. Closing resolved tickets after confirmation.
10. Identifying recurring incidents for problem management.

---

# 3. Ticket Categories

All incoming tickets should be assigned an appropriate category.

| Category | Examples |
|---|---|
| Account & Access | Password reset, account locked |
| Hardware | Laptop, keyboard, monitor, printer |
| Software | Application installation, application crash |
| Network | Wi-Fi, LAN, DNS, connectivity |
| VPN | VPN connection or authentication problems |
| Security | Phishing, malware, suspicious activity |
| Email | Email access, delivery problems |
| Remote Access | Remote desktop, corporate systems |
| Data & Storage | File access, shared drive |
| Other | Issues that do not fit another category |

---

# 4. Incident Priority

Tickets should be prioritized according to business impact and urgency.

### Priority 1 — Critical

Used when a major business service is unavailable or there is a serious security incident.

Examples:

- Company-wide network outage.
- Production system unavailable.
- Major security incident.
- Ransomware or malware outbreak.
- Critical business application unavailable for multiple users.

**Action:** Immediately escalate to the appropriate technical and security teams.

---

### Priority 2 — High

Used when an important service is unavailable for multiple users or significantly affects business operations.

Examples:

- Department-wide application outage.
- VPN unavailable for a large group.
- Multiple employees unable to access an important system.

**Action:** Begin troubleshooting immediately and escalate if first-level troubleshooting does not resolve the issue.

---

### Priority 3 — Medium

Used for issues affecting one employee or a small number of users without major business disruption.

Examples:

- Individual VPN issue.
- Application error.
- Laptop performance issue.
- Printer problem.

**Action:** Troubleshoot according to the relevant procedure.

---

### Priority 4 — Low

Used for general requests or issues with minimal business impact.

Examples:

- Software installation request.
- General IT question.
- Minor configuration request.
- Non-urgent hardware request.

**Action:** Process according to normal service request procedures.

---

# 5. Standard Ticket Handling Process

The Service Desk should follow these steps for every ticket.

## Step 1 — Receive Request

Obtain the following information:

- Employee name.
- Employee ID if applicable.
- Department.
- Contact information.
- Description of the issue.
- Time the issue started.
- Error message, if available.
- Affected device or application.
- Number of affected users.

---

## Step 2 — Create Ticket

Create a service desk ticket containing:

- Ticket ID.
- User information.
- Category.
- Priority.
- Issue description.
- Date and time.
- Assigned technician.
- Initial troubleshooting steps.

---

## Step 3 — Verify the Problem

Ask the user to describe what happened.

Confirm:

- What is not working?
- When did it start?
- Does the problem happen every time?
- Is anyone else experiencing the same issue?
- Was anything changed recently?

---

## Step 4 — Perform Initial Troubleshooting

Use approved troubleshooting procedures.

Common first-level actions include:

- Restarting the affected application.
- Restarting the computer.
- Checking network connectivity.
- Verifying account status.
- Checking available storage.
- Checking service status.
- Reviewing error messages.
- Confirming configuration settings.

Do not make unauthorized security or system changes.

---

## Step 5 — Document the Resolution

Record:

- Troubleshooting performed.
- Root cause, if known.
- Solution applied.
- User confirmation.
- Any follow-up action required.

---

## Step 6 — Close the Ticket

A ticket can be closed when:

1. The issue has been resolved.
2. The user confirms resolution, where required.
3. All troubleshooting information has been documented.
4. No further action is required.

---

# 6. Password Reset Procedure

## Symptoms

The employee may report:

- Forgotten password.
- Account locked.
- Password expired.
- Unable to authenticate.

## Procedure

1. Verify the employee's identity using the approved identity verification process.
2. Check the account status.
3. Determine whether the account is locked or the password has expired.
4. Perform the password reset using the approved identity-management system.
5. Ask the employee to create a new password if required.
6. Confirm that the employee can authenticate successfully.
7. Document the resolution.

### Security Rule

Never request or record the employee's password in a ticket.

---

# 7. VPN Troubleshooting Procedure

## Symptoms

Common symptoms include:

- VPN does not connect.
- Authentication failure.
- VPN disconnects frequently.
- Internal company resources cannot be accessed.

## Procedure

1. Confirm that the employee has an internet connection.
2. Confirm that the VPN client is installed and running.
3. Verify the employee's account is active.
4. Check whether the VPN service is experiencing an outage.
5. Ask the employee to restart the VPN client.
6. If required, restart the computer.
7. Verify the VPN configuration.
8. Attempt the connection again.
9. Check whether internal resources are accessible.
10. Escalate if the problem continues.

---

# 8. Software Installation Request

## Procedure

1. Confirm the requested application.
2. Check whether the application is approved.
3. Verify that the employee has authorization to use the application.
4. Check software licensing requirements.
5. Install the application using the approved software-management process.
6. Verify that the application launches successfully.
7. Confirm that the employee can use the application.
8. Record the installation in the ticket.

### Security Rule

Do not install unauthorized or unlicensed software on company devices.

---

# 9. Laptop Troubleshooting

## Common Symptoms

- Laptop is slow.
- Laptop does not start.
- Applications freeze.
- Device overheats.
- Blue screen or system crash.
- Battery problems.

## Initial Troubleshooting

1. Ask whether the problem is intermittent or continuous.
2. Restart the laptop.
3. Check available disk space.
4. Check whether excessive applications are running.
5. Check for operating-system updates.
6. Check for hardware error messages.
7. Check whether the problem started after a recent software or hardware change.
8. Run approved diagnostic tools.
9. Escalate hardware failures to the hardware support team.

---

# 10. Network Troubleshooting

## Symptoms

- No internet connection.
- Slow network.
- Unable to access internal resources.
- Wi-Fi frequently disconnects.

## Procedure

1. Check whether the device is connected to the correct network.
2. Check Wi-Fi or Ethernet status.
3. Test access to a known website.
4. Test access to an internal resource.
5. Restart the network adapter if appropriate.
6. Restart the device.
7. Check whether other employees are experiencing the same problem.
8. Check for a known network outage.
9. Escalate widespread outages to the network team.

---

# 11. Email Troubleshooting

## Common Problems

- Cannot send email.
- Cannot receive email.
- Email application does not open.
- Authentication failure.
- Mailbox storage limit reached.

## Procedure

1. Verify internet connectivity.
2. Check account status.
3. Confirm that the mailbox is active.
4. Check mailbox storage.
5. Verify email configuration.
6. Restart the email application.
7. Test webmail if available.
8. Check whether the issue affects other users.
9. Escalate server-side problems to the appropriate team.

---

# 12. Printer Troubleshooting

## Procedure

1. Confirm that the printer is powered on.
2. Check the network connection.
3. Check for paper or hardware errors.
4. Check printer status on the employee's computer.
5. Verify the correct printer is selected.
6. Clear stuck print jobs if authorized.
7. Restart the print service or device if appropriate.
8. Print a test page.
9. Escalate hardware failures to the printer support team.

---

# 13. Security Incident Procedure

Security-related tickets must be treated with high priority.

Examples include:

- Suspected phishing email.
- Malware detection.
- Suspicious login.
- Lost or stolen laptop.
- Unauthorized access.
- Suspicious files or applications.
- Accidental disclosure of sensitive information.

## Procedure

1. Do not ignore or close the ticket as a normal IT issue.
2. Record the available information.
3. Preserve relevant evidence.
4. Avoid deleting suspicious files unless instructed by the security team.
5. Escalate immediately to the security team.
6. Follow the company's incident-response procedure.
7. Restrict access or isolate the device only when authorized by the security team.
8. Document all actions.

### Important

Employees should never be asked to investigate suspected security incidents themselves.

---

# 14. Lost or Stolen Device

If an employee reports a lost or stolen company laptop or mobile device:

1. Verify the employee's identity.
2. Record the device details.
3. Record the approximate time and location of the loss if available.
4. Notify the security team immediately.
5. Initiate approved device-lock or remote-wipe procedures when authorized.
6. Disable or protect affected accounts when required.
7. Determine whether sensitive company information may have been exposed.
8. Escalate according to the security incident procedure.
9. Document all actions in the ticket.

---

# 15. When to Escalate

Escalate a ticket when:

- The issue cannot be resolved using the Service Desk procedure.
- Administrator privileges are required.
- The issue affects multiple users.
- A critical business service is unavailable.
- A security incident is suspected.
- Hardware replacement is required.
- The problem requires specialized technical knowledge.
- The issue has exceeded the defined service-level target.

---

# 16. Escalation Teams

| Issue | Escalation Team |
|---|---|
| Network outage | Network Team |
| Server problem | Infrastructure Team |
| Security incident | Security Team |
| Hardware failure | Hardware/Desktop Support |
| Application failure | Application Support Team |
| Database problem | Database Team |
| Identity/access problem | IAM Team |
| Cloud infrastructure issue | Cloud/Infrastructure Team |

---

# 17. Ticket Documentation Standard

Every ticket should contain enough information for another technician to understand the issue.

### Recommended Format

**Problem:**  
Describe the user's issue.

**Impact:**  
Describe who or what is affected.

**Troubleshooting:**  
List the steps performed.

**Result:**  
Describe what happened after troubleshooting.

**Resolution:**  
Describe the final solution.

**Escalation:**  
If escalated, record the team and reason.

---

# 18. Example Ticket

**Ticket ID:** INC-10045

**Category:** VPN

**Priority:** P3 — Medium

**Problem:**  
Employee cannot connect to the corporate VPN from home.

**Troubleshooting:**

1. Confirmed internet connection.
2. Confirmed VPN client was running.
3. Restarted VPN client.
4. Verified employee account was active.
5. Restarted laptop.
6. Attempted VPN connection again.

**Result:**  
VPN successfully connected after restarting the client.

**Resolution:**  
VPN client restart resolved the issue.

**Status:** Closed

---

# 19. Service Desk Best Practices

Service Desk technicians should:

- Verify user identity before sensitive account actions.
- Never request passwords.
- Follow approved procedures.
- Document troubleshooting steps.
- Protect confidential information.
- Use least-privilege access.
- Escalate security incidents immediately.
- Communicate clearly with employees.
- Avoid making unauthorized system changes.
- Keep tickets updated.
- Confirm resolution before closing important incidents.

---

# 20. Quick Reference

| Issue | First Action | Escalate When |
|---|---|---|
| Password reset | Verify identity and reset password | Account/IAM issue |
| VPN | Check internet and VPN client | VPN service/outage |
| Software | Verify approval and license | Application issue |
| Laptop | Restart and run basic diagnostics | Hardware failure |
| Network | Check connection and outage | Multiple users affected |
| Email | Check connectivity and account | Server-side issue |
| Printer | Check power/network/status | Hardware failure |
| Malware | Preserve information and escalate | Immediately |
| Lost laptop | Report and protect device/account | Immediately |
| Application crash | Restart and check errors | Persistent failure |

---

# 21. Important Security Rules

The following rules apply to all Service Desk operations:

1. Never ask users for their passwords.
2. Never store passwords in tickets.
3. Verify identity before account changes.
4. Do not install unauthorized software.
5. Do not disclose confidential company information.
6. Do not disable security controls without authorization.
7. Report suspected security incidents immediately.
8. Follow least-privilege principles.
9. Document administrative actions.
10. Escalate anything outside the technician's authorization level.

---

# 22. Document Control

**Document Owner:** IT Service Desk  
**Version:** 1.0  
**Status:** Active  
**Review Frequency:** Periodic review by IT management  
**Classification:** Internal Use

This runbook should be updated whenever Service Desk procedures, security requirements, systems, or escalation processes change.