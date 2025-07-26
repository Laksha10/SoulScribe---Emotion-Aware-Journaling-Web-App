# **SoulScribe** 🕊️  
*A Privacy-First Emotion-Aware Journaling Platform*  

SoulScribe is a journaling web application that combines **fine-tuned deep learning models** with a **Flask + PostgreSQL backend** and a **Streamlit-based interactive dashboard**.  
It helps users **track emotional patterns, visualize emotional arcs, and detect negative spirals** while providing **personalized coping strategies and escalation alerts** when necessary.

---

## **Features**
- **Emotion-Aware Journaling** – Entries are analyzed using a fine-tuned **RoBERTa‑Large model** (28 emotions) for precise emotion tagging.  
- **Companion Responses via LLMs** – Context-aware responses generated using **Google Gemini** and **Hugging Face Transformers**, guided by the detected emotions.  
- **Adaptive Alerts & Escalation** – Tracks negative emotional spirals, triggers **Red Zone alerts**, and escalates to support contacts via **SendGrid email integration**.  
- **Emotion Arc & Timeline Visualizations** – Visualizes emotional patterns across sessions, including session‑wise emotion tracking and an emotion scoreboard for deeper insights.  
- **Privacy‑First Design** – Secure user authentication & **PostgreSQL + Supabase backend** for encrypted storage of user data.  

---

## **Tech Stack**
- **Frontend**: Streamlit (interactive dashboards for journaling & analytics)  
- **Backend**: Flask (REST API), PostgreSQL, Supabase  
- **ML/NLP**: RoBERTa‑Large (emotion classification), **Google Gemini** & Hugging Face Transformers (for emotion-driven companion responses)  
- **Integrations**: SendGrid (escalation emails), SQLAlchemy ORM  
- **Visualization**: Plotly (emotion arc, timeline, and scoreboard)  

---

## **System Architecture**
- **Frontend**: Streamlit (interactive dashboards, emotion visualizations)  
- **Backend**: Flask REST API  
- **Database**: PostgreSQL (hosted via Supabase)  
- **Modeling**: HuggingFace Transformers (RoBERTa-Large)  

---
### 📦 Git LFS Setup (Required for Model File)

This project uses [Git Large File Storage (LFS)](https://git-lfs.github.com/) to manage large files like the emotion model (`model_weights.pt`).

Make sure you install and initialize Git LFS **before cloning** the repository:

```bash
# Install Git LFS (macOS example using Homebrew)
brew install git-lfs

# Initialize Git LFS
git lfs install
```
---

## **Installation & Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/Laksha10/SoulScribe---Emotion-Aware-Journaling-Web-App.git
   ```
---
## **How to Use SoulScribe**

#### 🔐 Registration  
Begin by creating your personal SoulScribe account.

<div style="display: flex; justify-content: center; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
  <img src="https://github.com/user-attachments/assets/56e27ca1-0d2e-4cc5-a51d-e15822f3e398" style="width: 45%;" />
  <img src="https://github.com/user-attachments/assets/6f58f7a5-5499-49cb-b925-7b39d2cb57fe" style="width: 45%;" />
</div>


#### 🔑 Login  
Securely log in and get started with your journaling dashboard.

<div align="center">
  <img src="https://github.com/user-attachments/assets/ed6d863c-02c2-4076-96b9-482595a0098c" width="40%" />
</div>

### 📔 Add Journal Entries  
Write your thoughts, feelings, and reflections.
<div align="center">
  <img src="https://github.com/user-attachments/assets/1e78516c-49fd-406e-867c-e1edca8af6f9" width="50%" />
</div>

### 📊 Track Your Emotional Arc  
Visualize emotional progression across sessions.
<div align="center">
  <img src="https://github.com/user-attachments/assets/99468214-d176-4913-852b-539f00f86728" width="45%" />
</div>


### 🎯 Session Scoreboard  
Get a session-wise breakdown of emotional states.
<div align="center">
  <img src="https://github.com/user-attachments/assets/ecc6dd22-a6ef-4edb-9e98-cd06123a1e36" width="50%" />
</div>


### 🧭 Timeline View  
See thread-wise and session-wise entries at a glance.
<div align="center">
  <img src="https://github.com/user-attachments/assets/2c906ea4-5136-4295-932f-3de45c9dc88d" width="50%" />
</div>


### 🚨 Red Zone Alerts  
Receive alerts when emotional spirals are detected.
<div align="center">
  <img src="https://github.com/user-attachments/assets/bc2ca870-83ef-4f90-b0c0-0fb098c9a3e8" width="50%" />
</div>


### 🧑‍🤝‍🧑 Support Contact & Email Escalation  
Configure a trusted support contact. If repeated distress is detected, SoulScribe automatically escalates by sending them an alert email via SendGrid.
<div align="center">
  <img src="https://github.com/user-attachments/assets/afe1f2ab-dae8-406e-9548-fe578cb0b6d1" width="50%" />
</div>


## 📄 License

This project is licensed under a **Custom Non-Commercial License**.  
The source code is provided solely for reference and feedback purposes.  
Deployment, redistribution, or commercial use is strictly prohibited without written permission.

For licensing inquiries or commercial use, please contact: singlalaksha10@gmail.com

