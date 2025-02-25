# IDOR Vulnerability in Workplace Portal

## ⚠️ Disclaimer
This is for educational and research purposes only. I do not encourage or support unauthorized access to any system. 

## 🛠 The Vulnerability
While exploring a workplace portal, I discovered an **IDOR (Insecure Direct Object Reference)** vulnerability that allowed unauthorized access to employee-sensitive data.

### 🔍 How It Works
- Each workplace has a unique numeric place id (`/EmployeeList.aspx?place_id=123`)
- The system does NOT check if the logged-in user is authorized to access other workplaces.
- Changing the `place_id` in the URL lets anyone see employees' full names, emails, and phone numbers.

### 🕸️ The Scraper
This script is for educational and research purposes only and demonstrates how an insecure IDOR implementation can expose sensitive workplace data.
- It shows how an attacker could enumerate workplaces using sequential `place_id` values.
- The script is designed to highlight the security flaw IDOR, not to be used for malicious purposes.
- No real credentials, exploits, or unauthorized actions are included.

**📌 Companies should fix this issue by implementing proper authorization checks to restrict access to sensitive data.**
