# AutoPyNet

> **Automate. Simplify. Thrive.**
> A Python-based network automation tool for securely pushing configuration updates and software/firmware upgrades to Cisco routers, switches, and firewalls, using Zero Touch Provisioning (ZTP), SSH, and Multi-Factor Authentication (MFA).

**Final Year Project (FYP)** · Department of Computer Science · Batch Fall 2026

---

## Overview

Manually updating multiple Cisco devices is slow, error-prone, and risky, especially in multi-branch organizations. **AutoPyNet** automates this process for small and medium-sized enterprises (SMEs):

- **ZTP** onboards new or existing Cisco devices and delivers updates with minimal human effort.
- **SSH** gives encrypted, reliable communication between the tool and the devices.
- **MFA** ensures only authorized personnel can trigger configuration changes or firmware upgrades.

The system is first built and tested in a controlled **LAN / Head Office (HO)** environment, then extended to a **multi-branch** setup with centralized management.

## Key Features

- Push configuration, software, and firmware updates to multiple Cisco devices at once
- Zero Touch Provisioning for automated device onboarding
- MFA-protected access to the application
- SSH-based secure command and file transfer (Paramiko / Netmiko / SCP)
- Centralized management from LAN/HO to multi-branch networks
- Logging, error handling, and verification of pushed changes
- Reduced manual effort, human error, and downtime

## Objectives

1. Build a tool that pushes software, firmware, and configuration updates to many Cisco devices simultaneously.
2. Implement ZTP for automated onboarding and update delivery.
3. Integrate MFA to secure access to the AutoPyNet system.
4. Use SSH for encrypted communication with devices.
5. Deploy and validate in a LAN/HO environment first.
6. Extend to multi-branch environments with centralized control.
7. Reduce manual effort, human errors, and operational downtime.
8. Serve as a practical learning platform for network automation and secure Python scripting.

## Scope

| In scope | Out of scope |
| --- | --- |
| Cisco routers, switches, and firewalls | Non-Cisco / multi-vendor support |
| ZTP-based provisioning | Orchestration tools (Ansible Tower, Cisco DNA Center) |
| MFA + SSH security | Cloud / SaaS deployment |
| Phase 1: LAN/HO, Phase 2: multi-branch | AI anomaly detection, real-time monitoring dashboards |

## System Architecture

```
 Network Admin ──► MFA Login ──► AutoPyNet Server (Python)
                                   ├── Device Handler (SSH: Paramiko / Netmiko)
                                   ├── ZTP Module (onboarding + config delivery)
                                   ├── Update Engine (config / firmware push, SCP)
                                   └── Logger & Verification
                                          │
                     ┌────────────────────┼────────────────────┐
                  Routers              Switches             Firewalls
                    (Cisco devices: LAN/HO → multi-branch)
```

## Tech Stack

| Category | Tools |
| --- | --- |
| Language | Python 3.x |
| Device communication | Paramiko, Netmiko, SCP |
| MFA | pyotp / Authlib / Flask or Django-based MFA |
| Simulation & testing | EVE-NG, Cisco IOS / IOS-XE devices |
| Version control | Git, GitHub |
| IDE | VS Code / PyCharm |

## Installation

```bash
git clone https://github.com/arham2k4/AutoPyNet-FYP.git
cd AutoPyNet-FYP

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

**Prerequisites**
- Python 3.9+
- Network reachability from the AutoPyNet server to the target Cisco devices
- SSH enabled on devices (or a ZTP-capable device for onboarding)
- EVE-NG lab or physical Cisco devices for testing

## Usage

```bash
python main.py
```

1. Log in with your credentials and complete the MFA verification.
2. Add or select the target Cisco devices (router / switch / firewall).
3. Choose the configuration or firmware update to push.
4. Run the update and monitor the logs/output.
5. Verify the result using the built-in verification commands.

> Update the commands above to match your actual entry point and file names.

## Project Phases

- **Phase 1:** Implementation, testing, and validation in a LAN/HO environment
- **Phase 2:** Extension to a multi-branch environment with centralized management

## Project Timeline (2026–2027)

| Stage | Activities |
| --- | --- |
| Requirement analysis & planning | Literature review, Cisco device study, define ZTP/MFA/SSH requirements |
| System design | Architecture (LAN → multi-branch), database/logging design |
| Implementation | SSH module, ZTP integration, MFA, update-pushing logic |
| Testing & validation | Unit/integration tests, security tests (MFA + SSH), multi-branch simulation |
| Deployment & optimization | LAN/HO deployment, multi-branch extension |

## Future Work

- Broader device compatibility (multi-vendor)
- Intelligent update scheduling
- Integration with advanced automation frameworks
- Real-time monitoring dashboard

## SDG Alignment

- **SDG 4:** Quality Education
- **SDG 8:** Decent Work and Economic Growth
- **SDG 9:** Industry, Innovation and Infrastructure
- **SDG 16:** Peace, Justice and Strong Institutions
- **SDG 17:** Partnerships for the Goals
