import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ---- Your imports ----
from DataLayer.BruteForceretriver import BruteForceRetriever
from DataLayer.DataManager import DataManager
from DataLayer.PickleStore import PickleBackend
from DataLayer.SentenceTransformerModel import SentenceTransformerModel
from LLMLayer.OllamaLLM import OllamaLLM
from promptLogger import PromptLogger
from MainBot import RAGBot

import os
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not set")

# ---------- Setup RAG (same as maintest) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
knowledge_path = os.path.join(BASE_DIR, "MyKnowledge")
store_path = os.path.join(BASE_DIR, "store.pkl")

embed_model = SentenceTransformerModel()
llm = OllamaLLM("mistral", base_url="http://localhost:11434")
db = PickleBackend(path=store_path)
dm = DataManager(knowledge_path, db, embed_model, 400, 100)

if not dm.is_synced():
    dm.sync()

data = db.get_all()
retriever = BruteForceRetriever(data["chunks"], data["embeddings"])
logger = PromptLogger()

bot = RAGBot(llm, retriever, embed_model, logger)

# ---------- Telegram Handlers ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👕 Hi! Ask me anything about t-shirts!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text

    response = bot.answer_query(
        user_id=str(update.effective_user.id),
        session_id=str(update.effective_chat.id),
        user_query=user_query
    )

    await update.message.reply_text(response)

# ---------- Main ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Telegram bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()  