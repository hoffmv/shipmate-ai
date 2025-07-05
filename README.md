# Shipmate AI

**Shipmate** is a modular, agent-based personal AI system designed to manage every dimension of your life — finance, scheduling, communication, trading, fitness, and more.

> This repository contains the full system, including backend, agents, frontend, and utilities.

---

## 🔧 Features

- 💸 Personal Finance Command (Gold Digger Division)
- 🕰️ Smart Scheduling & Conflict Management (Time Lords Division)
- 📊 Automated 401(k) Allocations Based on Risk Profile
- 🧠 Modular AI Experts (e.g., `CryptoTraderAgent`, `SmartSchedulerAgent`)
- 📅 Calendar Sync with Event Prioritization
- 📦 Persistent Memory Storage

---

## 🚀 Local Setup

### 1. Clone Repo

```bash
git clone https://github.com/hoffmv/shipmate-ai.git
cd shipmate-ai

2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate  # On Windows

3. Install Requirements
pip install -r requirements.txt

4. Run the System
python app.py


📱 Mobile Access
Coming soon: Progressive Web App (PWA) and/or mobile-optimized bot wrapper.

📂 Project Structure (Simplified)
bash
Copy
Edit

shipmate-ai/
│
├── backend/
├── frontend/
├── core/
├── utils/
├── templates/
├── agents_*/      # Domain-specific AI agents
├── app.py
└── requirements.txt

📜 License
Custom use only – not for commercial redistribution.


