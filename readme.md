# Steps to Set up the Bot

1. set-up ollama 
2. ollama pull mistral
3. python  -m venv myenv
4. activate the env
5. pip install -r requirements.txt
6. python DataLayer/testData.py -- test DataLayer
7. python LLMLayer/testLLM.py  -- test LLMLayer
8. setx TELEGRAM_BOT_TOKEN "your_actual_token_here"  --(Get this from @botFather on telegram)
9. run main.py
10. Go the telegram bot and ask querry.

# Telegram bot instructions

| Command                 | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| /ask <query>           | Runs the RAG query; shows a warning if no query is provided                |
| /help                  | Displays formatted usage instructions                                      |
| /start                 | Resumes the bot for that chat (sets polling active)                        |
| /quit                  | Pauses the bot for that chat (ignores /ask and free-text)                  |