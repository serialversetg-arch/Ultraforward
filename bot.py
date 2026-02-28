import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

# Advanced Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client("AdvancedForwarder", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- START COMMAND ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = (
        "<b>✨ Welcome to Auto Forwarder Bot ✨</b>\n\n"
        "🤖 <u><b>Bot Status:</b></u> <code>Running Active ✅</code>\n"
        "📂 <b>Task:</b> Replacing Tags & Forwarding\n\n"
        "📌 <b>Target Tag:</b> <code>{}</code>\n"
        "🚀 <b>New Tag:</b> <code>{}</code>\n\n"
        "<i>Power by @Hindi_Tv_Verse</i>".format(OLD_TAG, NEW_TAG)
    )
    
    # Adding a stylish button
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Channel", url="https://t.me/Hindi_Tv_Verse")]
    ])
    
    await message.reply_text(text, reply_markup=button)

# --- AUTO FORWARD & REPLACE LOGIC ---
@app.on_message(filters.chat(SOURCE_CHAT) & (filters.video | filters.document))
async def handle_forward(client, message):
    try:
        # Caption check
        caption = message.caption if message.caption else ""
        
        # Replace logic
        if OLD_TAG in caption:
            new_caption = caption.replace(OLD_TAG, f"<b>{NEW_TAG}</b>")
        else:
            new_caption = f"{caption}\n\n✨ <b>{NEW_TAG}</b>"

        # Stylish Forwarding with Copy
        await message.copy(
            chat_id=TARGET_CHAT,
            caption=new_caption,
            parse_mode="html"
        )
        logger.info(f"✅ Successfully Processed: {message.id}")

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")

print("⚡ Bot Started Successfully!")
app.run()
