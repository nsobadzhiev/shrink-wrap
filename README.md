# 🤖 ShrinkWrap
## CustomGPT Telegram Bot

CustomGPTs are just glorified system prompts. There's no reason you shouldn't be able to run one yourself, without having a ChatGPT Plus subscription.

As long as you have an API Key or a way to run the bot with a locally running LLM, you can create your own CustomGPT and expose it as a Telegram bot.

---

### 🚀 Features

- Telegram integration 
- GPT-4o or any LiteLLM-supported LLM backend
- Easy environment-based configuration

---

### 🛠️ Getting Started

#### 1. Clone the Repository

```bash
git clone https://github.com/nsobadzhiev/customgpt-telegrambot.git
cd customgpt-telegrambot
```

---

#### 2. Create a Telegram Bot via BotFather

1. Open Telegram and search for [@BotFather](https://t.me/BotFather).  
2. Start a conversation and run the `/newbot` command.  
3. Choose a name and username for your bot.  
4. BotFather will give you a **token** like:  
   `85451:ABCDEF1234567890xyz`  
5. Save this token — you'll use it in the `.env` file below.  

---

#### 3. Create `.env` File

In the root directory, create a `.env` file with the following structure:

```env
# Telegram
TOKEN=85451:ABCDEF1234567890xyz
DOMAIN=your-public-url.trycloudflare.com

# LiteLLM
MODEL=openai/gpt-4o
API_KEY=sk-your-liteLLM-api-key
# Optional if not using OpenAI or cloud-hosted model:
# LLM_API_BASE=http://localhost:11434

CUSTOM_GPT_NAME=candidate_job_fit
```

> 💡 Use [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/) or [ngrok](https://ngrok.com/) to expose your local FastAPI server to the internet for Telegram webhook support.

---

#### 4. Install Dependencies (using `uv`)

[`uv`](https://github.com/astral-sh/uv) is the recommended way to manage dependencies for this project.

---

#### 5. Run the Bot

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Once running, your bot will start responding to Telegram messages.

---

### 📬 Webhook Setup

Telegram bots require a publicly accessible URL. Once your FastAPI app is running and accessible via your `DOMAIN`, the bot will automatically register the webhook using the `TOKEN`.

---

### 📄 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

### 🙌 Contributions

Pull requests, issues, and ideas are welcome! If you find bugs or want to add features, feel free to open a PR.
