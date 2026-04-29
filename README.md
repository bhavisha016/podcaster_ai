# 🎙️ AI Agent-Based Podcast Generator

## 🚀 Overview
This project is an AI-powered multi-agent system that automatically generates short podcast scripts from a given topic and converts them into audio. It uses LLMs via Groq and CrewAI to simulate a workflow of research → analysis → content generation → audio delivery.

## ⚙️ How It Works
Input Topic → Research Agent → Reporting Agent → Script Writing Agent → Audio Generation (TTS) → Telegram Delivery

## 🧠 Architecture
This system is built using a multi-agent architecture:
- Researcher: gathers relevant information about the topic  
- Reporting Analyst: converts raw information into structured insights  
- Script Writer: generates a podcast-ready script  

LLM backend is powered by Groq (llama-3.1-8b-instant).  
Audio is generated using Groq TTS API.  
Final output is delivered using Telegram Bot API.

## 📂 Project Structure
podcaster_ai/
│
├── src/podcaster/
│   ├── crew.py              # Agent + task orchestration
│   ├── main.py              # Entry point
│   ├── tools.py             # Utility tools
│   ├── delivery/
│   │   └── telegram_bot.py  # Telegram integration
│   └── config/
│       ├── agents.yaml
│       └── tasks.yaml
│
├── outputs/                 # Generated scripts & audio
├── .env                     # API keys
└── README.md

## ▶️ How to Run

1. Create virtual environment  
python -m venv venv  
venv\Scripts\activate  

2. Install dependencies manually (if not already installed)  
pip install crewai python-dotenv requests crewai-tools  

3. Add .env file  
GROQ_API_KEY=your_key  
TELEGRAM_BOT_TOKEN=your_token  
CHAT_ID=your_chat_id  

4. Run the project  
python -m src.podcaster.main  

## 📡 Output
- Script → outputs/script-*.md  
- Report → outputs/report-*.md  
- Audio → outputs/podcast-latest.wav  
- Automatically sent to Telegram  

## ⚠️ Limitations
- Single voice audio (no multi-speaker support)  
- Limited by API rate limits (Groq free tier)  
- Short podcast duration (~30–60 seconds)  

## 💡 Future Improvements
- Multi-voice conversation support  
- Web UI (Streamlit / Dashboard)  
- Database integration  
- Automated scheduling (daily podcasts)  
- RAG for real-time knowledge  

## 🧠 Key Concepts Used
- Multi-Agent Systems  
- LLM Orchestration  
- Prompt Engineering  
- API Integration  
- Pipeline Automation  

## 📌 Resume Description
Built a multi-agent AI system using CrewAI and Groq LLMs to automate content generation, script creation, and audio delivery via Telegram.

## 👤 Author
Your Name
