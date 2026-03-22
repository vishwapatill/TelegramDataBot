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

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not set")

# ---------- Setup RAG ----------
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

# ---------- Per-chat polling state ----------
# Tracks which chat IDs have polling enabled (True) or paused (False)
polling_enabled: dict[str, bool] = {}


def is_polling_active(chat_id: str) -> bool:
    """Returns True if the chat has not explicitly paused polling."""
    return polling_enabled.get(chat_id, True)


# ---------- Command Handlers ----------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /Start — Resume polling / greet the user.
    Sets the chat's polling state to active.
    """
    chat_id = str(update.effective_chat.id)
    polling_enabled[chat_id] = True
    await update.message.reply_text(
        "✅ Bot is active!\n\n"
        "Use /ask <your question> to query the knowledge base, "
        "or /help for full usage instructions."
    )


async def cmd_quit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /Quit — Pause polling for this chat.
    The bot will ignore /ask and free-text messages until /Start is used.
    """
    chat_id = str(update.effective_chat.id)
    polling_enabled[chat_id] = False
    await update.message.reply_text(
        "⏸️ Bot paused. Send /Start to resume."
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /help — Show usage instructions.
    """
    help_text = (
        "🤖 *RAG Bot — Usage Guide*\n\n"
        "*Commands:*\n"
        "• `/ask <query>` — Ask a question using the knowledge base (RAG)\n"
        "• `/Start` — Resume the bot after it has been paused\n"
        "• `/Quit` — Pause the bot (ignores messages until /Start)\n"
        "• `/help` — Show this help message\n\n"
        "*Examples:*\n"
        "`/ask What materials are used in the shirts?`\n"
        "`/ask How do I choose the right size?`\n\n"
        "You can also send a plain text message and the bot will answer it directly (when active)."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cmd_ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /ask <query> — Run a RAG query against the knowledge base.
    """
    chat_id = str(update.effective_chat.id)

    if not is_polling_active(chat_id):
        await update.message.reply_text(
            "⏸️ Bot is paused. Send /Start to resume."
        )
        return

    # Extract the query after /ask
    query = " ".join(context.args).strip() if context.args else ""
    if not query:
        await update.message.reply_text(
            "⚠️ Please provide a query.\n"
            "Usage: `/ask <your question>`",
            parse_mode="Markdown"
        )
        return

    await update.message.reply_text("🔍 Searching knowledge base...")

    response = bot.answer_query(
        user_id=str(update.effective_user.id),
        session_id=chat_id,
        user_query=query
    )

    await update.message.reply_text(response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Free-text message handler — behaves like /ask but without the command prefix.
    Ignored when the chat is paused.
    """
    chat_id = str(update.effective_chat.id)

    if not is_polling_active(chat_id):
        # Silently ignore messages while paused
        return

    user_query = update.message.text.strip()
    if not user_query:
        return

    response = bot.answer_query(
        user_id=str(update.effective_user.id),
        session_id=chat_id,
        user_query=user_query
    )

    await update.message.reply_text(response)


# ---------- Main ----------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", cmd_start))   # /start (Telegram default)
    app.add_handler(CommandHandler("Start", cmd_start))   # /Start (explicit casing)
    app.add_handler(CommandHandler("quit", cmd_quit))     # /quit
    app.add_handler(CommandHandler("Quit", cmd_quit))     # /Quit (explicit casing)
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("ask", cmd_ask))

    # Free-text fallback
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Telegram RAG bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()