# ⚖️ Advocacy ⚖️ : A Legal Practice Management Suite

  

> A full-featured desktop application for advocates to manage their cases, clients, hearings, fees, and legal knowledge — with both cloud and offline modes.

  

---

## 📑 Table of Contents

- [📋 Overview](#-overview)
- [🗄️ Dataset](#️-dataset)
- [🛠️ Tools & Technology](#️-tools--technology)
- [⚙️ Methods](#️-methods)
- [📊 Key Features](#-key-features)
- [🚀 How to Run This Project](#-how-to-run-this-project)
- [📈 Results & Conclusion](#-results--conclusion)
- [🔮 Future Work](#-future-work)
- [👤 Author & Contact](#-author--contact)

---

  

## 📋 Overview

  

**Advocacy** is a professionally designed desktop application built for advocates and law firms to digitize and streamline their entire legal practice. It replaces paper registers and scattered spreadsheets with a clean, unified platform covering case management, client records, fee tracking, expense logging, hearing calendars, and more.

  

The application ships in two versions:

-  **Cloud Mode** — data stored on Aiven Cloud MySQL, accessible from any machine

-  **Local Mode** — fully offline, data stored in SQLite on the user's PC, no internet needed

  

It supports **four user roles** — Advocate, Advocate's Assistant, Client and Admin — each with their own tailored dashboard and access controls.

  

A built-in **Bhartiya Nyaya Samhita (BNS) Knowledge Panel** provides advocates with quick-reference summaries of BNS sections directly on the home screen, rotating automatically every 2 minutes.

  

---

  

## 🗄️ Dataset

  

The application ships with pre-loaded demo data for the **`DemoAdv`** advocate account so new users can immediately explore all features without entering any data:

  

| Data | Count |
|---|---|
| Demo Clients | 25 (C009 – C033) Client id's |
| Demo Cases | 40 cases spread across all stages (filed, ongoing, disposed, settled) |
| Hearings | 150+ past & upcoming hearing records |
| Payments | 80+ payment records with generated receipts |
| Expenses | Court fees, photocopying, travel, notary charges |
| Pending Dues | Outstanding dues for all ongoing cases |
| BNS Sections | 342 Bhartiya Nyaya Samhita sections with summaries |
| Case Timeline Events | Full audit trail per case |

  

**Demo Login Credentials:**

  

| Role | Username | Password |
|---|---|---|
| Advocate | `DemoAdv` | `DemoPass` |
| Client | `C009` – `C033` | *(same as client ID)* |

  

---

  

## 🛠️ Tools & Technology

  

| Category | Technology |
|---|---|
| **Language** | Python 3.14 |
| **UI Framework** | CustomTkinter + Tkinter |
| **Cloud Database** | MySQL 8.4 on Aiven Cloud |
| **Local Database** | SQLite 3 |
| **PDF Generation** | ReportLab |
| **Password Security** | bcrypt (12 rounds) |
| **App Packaging** | PyInstaller |
| **Installer Builder** | Inno Setup 6 |
| **Cloud Hosting** | Aiven Cloud (MySQL, SSL-secured) |

  

---

  

## ⚙️ Methods

  

### Architecture

The application follows a **single-file monolith** architecture for portability — the entire application (6,500+ lines) is self-contained in one Python file per mode (Cloud/Local), making it trivially easy to package and distribute.

  

### Dual-Mode Database Layer

A single `DB` class abstracts all data access. The **Cloud version** uses `mysql.connector` to connect to Aiven's managed MySQL over SSL. The **Local version** uses Python's built-in `sqlite3` module with a row-factory that mimics MySQL's dictionary cursor, so all UI code is 100% identical across both versions.

  

### Role-Based Access Control (RBAC)

Four distinct dashboard classes — `AdvocateDashboard`, `AdminDashboard`, `ClientDashboard`, `AssistantDashboard` — are loaded at login based on the authenticated user's role. Advocate Assistants have **granular feature-level permissions** configurable per-assistant by the advocate (7 distinct feature keys).

  

### Installer System

The dual-mode installer (`AdvocacySetup.exe`) is built with **Inno Setup 6**. At installation time, the user picks Cloud or Local mode through a custom wizard page, with separate password gates for each mode.

  

### BNS Gyan Samvardhak Panel

342 BNS section records live in the database. On every home screen, a random section is displayed with section number, title, summary, category badge, and punishment severity. It auto-refreshes every 2 minutes with a countdown timer and supports a manual "Next Section" button.

  

---

  

## 📊 Key Features

  

### Advocate Dashboard

-  **Case Info** — full case details: court, judge, case type, filing date, status, last/upcoming dates, next step

-  **Add New Case** — register cases with all metadata in one form

-  **Update Case** — log new hearings, results, timeline events, update case status

-  **Ongoing Cases** — scrollable list of all active cases

-  **Fees Tracking** — view payment history and outstanding dues per case

-  **Expenses Log** — view court fees, travel, photocopying, notary charges per case

-  **Money Incoming** — record payments, generate PDF receipts, view full payment history

-  **Manage Clients** — register new clients, view all, manage linked accounts

-  **Manage Assistants** — create/delete assistants, configure per-feature permissions

-  **Account Settings** — change password, update profile

  

### Admin Dashboard

- All Advocate features, plus:

-  **Create Advocate Accounts** — invite-only; no self-registration

-  **Manage All Advocates & Assistants** — system-wide oversight

  

### Client Dashboard

- View own cases with full hearing history and case timeline

- Payment portal — view dues and payment receipts

  

### Assistant Dashboard

- Restricted access based on permissions granted by the linked advocate

- Up to 7 feature permissions: Case Info, Add Case, Update Case, Client Cases, Fees Tracking, Expenses, Money Incoming

  

### BNS — Gyan Samvardhak Panel

- Displayed on all four dashboard home screens

- 342 Bhartiya Nyaya Samhita sections with summaries, categories, punishment details

- Auto-rotates every 2 minutes | Manual "Next Section" button

  

---

  

## 🚀 How to Run This Project

  

### ⬇️ Option A — Download & Install (Recommended — No Setup Required)

The easiest way to get started. Just download and run the installer — no Python or coding knowledge needed.

1. Go to the repository: **[github.com/rsingh-bharat/advocacy](https://github.com/rsingh-bharat/advocacy)**
2. Click on **`AdvocacySetup.exe`** in the file list
3. On the file page, click the **⬇️ Download raw file** button (top-right of the file view)
4. Once downloaded, **right-click → Run as Administrator**
5. Choose **Cloud** (online, syncs across machines) or **Local** (fully offline)
6. Enter the installation password *(contact the author for password)*
7. Complete setup and launch Advocacy

> **Installer passwords:** Cloud: `rsingh82` | Local: `ronaksingh`

> 💡 **Tip:** If Windows shows a SmartScreen warning, click **"More info" → "Run anyway"** — this is normal for unsigned installers.

  

### Option B — Run from Source

  

**Prerequisites:**

```bash
pip install customtkinter reportlab mysql-connector-python bcrypt
```

  

**Cloud (MySQL) mode:**

```bash
git clone https://github.com/rsingh-bharat/advocacy.git
cd advocacy

# Import advocacy_db_v7_1.sql into your MySQL server
# Edit DB_CONFIG in ADVOCACY_v7_1.py with your host/port/user/password/database

python ADVOCACY_v7_1.py
```

  

---

  

## 📈 Results & Conclusion

  

Advocacy successfully delivers a **complete digital practice management system** for advocates:

  

- ✅ **End-to-end case lifecycle** — tracked from filing through hearings to disposal/settlement

- ✅ **100% offline-capable** — Local mode requires zero internet or server setup

- ✅ **Cloud-synced** — Cloud mode provides access from any machine via Aiven MySQL

- ✅ **Role-based access** — 4 distinct user roles with granular assistant permissions

- ✅ **Legal knowledge built-in** — 342 BNS sections always available on the home screen

- ✅ **Printable PDF receipts** — generated on the fly for every payment

- ✅ **One-file installer** — `.exe` installer with dual-mode wizard, fully password-protected

- ✅ **Real demo data** — 25 clients, 40 cases, 150+ hearings pre-loaded for DemoAdv

  

The platform eliminates dependence on paper registers, reduces missed hearings through calendar tracking, and gives clients transparent access to their own case progress.

  

---

  

## 🔮 Future Work

  

| Feature | Description |
|---|---|
| **Advocacy Web Version** | Browser-based access with the same full feature set |
| **e-Courts API Integration** | Auto-sync hearing dates from the e-Courts India public API |
| **Document Vault** | Attach scanned documents (FIR, judgments, affidavits) to cases |
| **Multi-Advocate Firm Mode** | Shared case pool with inter-advocate transfer and collaboration |
| **GST Invoicing** | Formal GST-compliant invoice generation for client billing |
| **Analytics Dashboard** | Case win/loss rates, revenue trends, hearing frequency charts |
| **Hearing Reminders** | Push/email/SMS notifications before upcoming hearing dates |
| **WhatsApp Alerts** | Notify clients of upcoming hearings via WhatsApp Business API |
| **Mobile App** | Android/iOS client app for advocates to access cases on the go |

  

---

  

## 👤 Author & Contact

  

**Ronak Singh**

Developer

  

- 📧 Email: *rsingh.bharat82@gmail.com*

- 🐙 GitHub: *[github.com/rsingh-bharat](https://github.com/rsingh-bharat)*

- 💼 LinkedIn: *[linkedin.com/in/rsingh-bharat](https://www.linkedin.com/in/rsingh-bharat)*

  

> *Built to give advocates the tools they deserve!!*

  

---

  

*⚖️ Advocacy Legal Practice Management Suite — v7.1*
# advocacy
