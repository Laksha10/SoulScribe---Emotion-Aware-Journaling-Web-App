# ✨ SoulScribe — Your Personal Emotion-Aware Journal

SoulScribe is an intelligent journaling assistant designed to understand your emotions through text, offer thoughtful reflections, and store your entries securely. Whether you're venting, celebrating, or just checking in with yourself, SoulScribe listens, understands, and responds.

---

## 🚀 Version 1 Highlights

- 🧠 **Emotion Detection:** Uses a fine-tuned transformer-based model to classify journal entries across multiple emotional categories.
- 📝 **Smart Journaling:** Generates tailored reflections or empathetic responses based on the detected emotional state.
- 🗄️ **Cloud Syncing:** Journal entries are stored securely in a Supabase PostgreSQL database.
- 🛠️ **Modular API Design:** Built with Flask, organized into blueprints for easy expansion and maintenance.

> This is Version 1 of SoulScribe. Performance optimization, additional features (like a richer response engine and frontend polishing), and enhanced database security are currently in progress and are expected to be completed within the next **10 days**.

---

## ⚙️ Tech Stack

- **Backend:** Flask + SQLAlchemy  
- **Database:** Supabase (PostgreSQL)  
- **ML Model:** Scikit-learn / Transformers  
- **Deployment-ready:** Clean architecture and environment-based config  

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/Laksha10/SoulScribe.git
cd SoulScribe

# 2. Set up a virtual environment
python3 -m venv soulscribe_env
source soulscribe_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file
# You can refer to .env.example for the necessary variables

# 5. Run the API
python app.py
