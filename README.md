# SecureVault

SecureVault is a Python-based password manager focused on secure credential storage, encryption, and desktop application development.

This project was built to practice:
- cybersecurity fundamentals
- encryption and authentication
- Python application development
- GUI design
- secure software architecture

---

# Features

## Authentication
- Master password login system
- SHA-256 password hashing
- Secure login verification

## Credential Management
- Add credentials securely
- View stored credentials
- Duplicate credential detection
- Password age tracking

## Password Security
- Random password generator
- Password strength analysis
- Encrypted password storage using Fernet encryption

## GUI Application
- Desktop GUI built with CustomTkinter
- Sidebar navigation system
- Modern dark-mode interface
- Dynamic page switching

---

# Technologies Used

- Python
- CustomTkinter
- Cryptography (Fernet)
- SHA-256 hashing

---

# Installation

Clone the repository:

```bash
git clone https://github.com/eristenn/SecureVault.git
cd SecureVault
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

## Windows
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python gui.py
```

---

# Screenshots

## Login Screen
<img width="401" height="332" alt="SecureVaultPic1" src="https://github.com/user-attachments/assets/7765d8a6-9edc-42d7-a9da-d29312181e97" />

## Dashboard
<img width="902" height="532" alt="SecureVaultPic2" src="https://github.com/user-attachments/assets/903b580d-a2fc-4e7f-81c3-9ecb2c6603a4" />

## Add Credential
<img width="902" height="532" alt="SecureVaultPic3" src="https://github.com/user-attachments/assets/3839b482-b26a-40ee-a80a-ded4e92cfc57" />

## View Vault
<img width="902" height="532" alt="SecureVaultPic4" src="https://github.com/user-attachments/assets/5764c6ac-33f4-4ffb-b0ad-73574d87df16" />

## Password Generator
<img width="902" height="532" alt="SecureVaultPic5" src="https://github.com/user-attachments/assets/6eea1ff6-7521-465c-b902-f8045ee0e0e7" />

---

# Future Features

- SQLite database integration
- Search functionality
- Delete/edit credentials
- Export as desktop executable (.exe)
- Security audit dashboard
- Custom themes and icons

---

# Version

Current Release:
```text
v0.2.0 — GUI Update
```

---

# Author

Developed by Eristen Forsythe.
