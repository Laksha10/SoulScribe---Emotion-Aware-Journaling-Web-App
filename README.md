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

---

## **Installation & Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/Laksha10/SoulScribe---Emotion-Aware-Journaling-Web-App.git
cd SoulScribe---Emotion-Aware-Journaling-Web-App
git lfs pull



## **How to Use SoulScribe**

### 📝 Sign Up & Login  
Create a secure account and start your journaling journey.

### 📔 Add Journal Entries  
Write your thoughts, feelings, and reflections.

### 📊 Track Your Emotional Arc  
Visualize emotional progression across sessions.

### 🎯 Session Scoreboard  
Get a session-wise breakdown of emotional states.

### 🧭 Timeline View  
See thread-wise and session-wise entries at a glance.

### 🚨 Red Zone Alerts  
Receive alerts when emotional spirals are detected.

### 🧑‍🤝‍🧑 Support Contact & Email Escalation  
Configure a trusted support contact. If repeated distress is detected, SoulScribe automatically escalates by sending them an alert email via SendGrid.
