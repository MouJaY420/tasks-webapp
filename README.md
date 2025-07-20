# 🏡 Tasks WebApp

A feature-rich Django + JavaScript web application to simplify everyday life at home.  
This app includes expense tracking with receipt scanning, task and floorplan management, and more to come.

## 🚀 Features

- 📸 **Expense OCR Upload**: Scan receipts from mobile and automatically extract line items.
- 🧾 **Smart Categorization**: Assigns items like "Tomatoes" to "Groceries" and "Soap" to "Cleaning".
- 🏠 **Modular Architecture**: Structured apps for `chores`, `expenses`, `floorplan`, `main`, and `core`.
- 📅 **Real-time Sync** (planned): Push receipt scans to desktop instantly using WebSockets or P2P.
- 🧱 **Modern Frontend**: Custom JS components and Webpack bundling for interactive UI.

## ⚙️ Tech Stack

- **Backend**: Django, Python
- **Frontend**: Vanilla JS, Webpack, html
- **OCR**: [Tesseract.js](https://github.com/naptha/tesseract.js) (or other — planned)
- **Database**: SQLite (development), Postgres (production target)
- **Other Tools**: Git, GitHub, SSH, PowerShell

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:MouJaY420/tasks-webapp.git
cd tasks-webapp
