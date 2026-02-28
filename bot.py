import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread
from config import *

# --- HEALTH CHECK SERVER (Port 8000 Fix) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Running Live!"

def run_web():
    # Koyeb/Heroku hamesha port 8000 ya 10000 check karte hain
    web_app.run(host="0.0.0.0", port=8000)

# Background mein server chalu karein
Thread(target=run_web).start()

# --- BOT LOGIC ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "AdvancedForwarder", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = (
        "<b>✨ Welcome to Auto Forwarder Bot ✨</b>\n\n"
        "🤖 <b>Status:</b> <code>Active ✅</code>\n"
        "🚀 <b>New Tag:</b> <code>{}</code>".format(NEW_TAG)
    )
    await message.reply_text(text)

@app.on_message(filters.chat(SOURCE_CHAT) & (filters.video | filters.document))
async def handle_forward(client, message):
    try:
        caption = message.caption if message.caption else ""
        # Replace logic
        new_caption = caption.replace(OLD_TAG, f"<b>{NEW_TAG}</b>") if OLD_TAG in caption else f"{caption}\n\n<b>{NEW_TAG}</b>"

        await message.copy(chat_id=TARGET_CHAT, caption=new_caption, parse_mode="html")
        logger.info(f"✅ Forwarded: {message.id}")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

print("⚡ Bot Starting with Port 8000 Bypass...")
app.run()
