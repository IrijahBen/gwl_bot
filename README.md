# 🌍 GWL Bot — Goodwill Language Solution Automated Backend

> A dual-channel, AI-powered customer support backend. Automates official WhatsApp Cloud API interactions and website chat enquiries using interactive menus and Groq's LLaMA 3.3 AI, ensuring no client goes unanswered.

---

## 🎯 What It Does

GWL Bot is an enterprise-grade automated backend built with FastAPI. It handles incoming customer requests via the **official Meta WhatsApp Cloud API** and a custom **Glassmorphism Web Chat Widget**. It guides users through interactive service menus (lists and buttons) and intelligently falls back on Groq's LLaMA 3.3 70B AI for custom inquiries, seamlessly handing over complex requests to human specialists.

---

## ✨ Features

- 📱 **Dual-Channel Support** — Operates simultaneously on WhatsApp (via Meta API) and your website (via custom HTML/JS widget).
- 🖱️ **Interactive Menus** — Fully automated, clickable UI flows (Lists and Quick Reply Buttons) so clients don't have to type out choices.
- 🤖 **AI-Powered Fallback** — Uses Groq LLaMA 3.3 70B for intelligent, context-aware responses when a user asks a custom question outside the menu flow.
- 👥 **Seamless Human Takeover** — Generates secure Reference Tokens and silently pauses the bot when a client requests a live agent, alerting your team in the Meta Business Suite.
- 🧠 **Session Memory** — Tracks user states (Bot mode vs. Human mode) and remembers conversation history for contextual AI replies.
- 🏢 **Business Focused** — Pre-configured for Goodwill Language Solution's document translation, interpretation, and language class services.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core backend language |
| **FastAPI & Uvicorn** | High-performance async web server & webhook router |
| **Meta WhatsApp API** | Official Cloud API for sending/receiving WhatsApp messages |
| **Groq API (LLaMA 3.3)** | Lightning-fast LLM for dynamic customer interactions |
| **HTML/CSS/JS** | Custom front-end web widget with a futuristic UI |
| **python-dotenv** | Secure environment variable management |

---

## 🚀 Getting Started (Local Development)

### 1. Clone the repository
```bash
git clone [https://github.com/IrijahBen/gwl_bot.git](https://github.com/IrijahBen/gwl_bot.git)
cd gwl_bot

```

### 2. Install dependencies

```bash
pip install -r requirements.txt

```

### 3. Set up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
WHATSAPP_ACCESS_TOKEN=your_meta_system_user_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=goodwill_secure_webhook_token_2026

```

### 4. Run the Server

Start the FastAPI application:

```bash
python app.py

```

The server will run on `http://0.0.0.0:8000`. You can open `index.html` in your browser to test the web widget locally.

---

## ☁️ Deployment (Render / Cloud)

This bot is optimized for deployment on cloud platforms like Render or Railway.

1. Connect your GitHub repository to Render as a **Web Service**.
2. Set the Build Command: `pip install -r requirements.txt`
3. Set the Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Add your `.env` variables in the Render dashboard.
5. Update your Meta Developer Dashboard with the generated secure `https://` webhook URL.

---

## 🗂️ Project Structure

```text
gwl_bot/
│
├── app.py             # Main FastAPI server, webhooks, and routing logic
├── index.html         # Front-end Web Chat Widget with Bottom Sheet Modal
├── requirements.txt   # Python dependencies
├── .env               # API keys and tokens (not pushed to GitHub)
├── .gitignore         # Ignores sensitive files and environments
└── README.md          # Project documentation

```

---

## 🧠 AI & Meta Integration

Unlike basic rule-based bots, GWL Bot leverages Meta's official interactive payloads to ensure a native, app-like experience on WhatsApp. If a user bypasses the menu, the integration with **Groq's LLaMA 3.3 70B** allows the bot to understand context, answer questions politely, and gracefully guide the user back to the official service menus.

---

## 👨‍💻 Author

**Ajiboye Abayomi Adewole (IrijahBen)**

GitHub: [@IrijahBen](https://github.com/IrijahBen)

```

```
