
from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
import asyncio
from config import api_id, api_hash, bot_token

bot = Client("cds_journey_final", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

user_tokens = {}

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "**CDS Journey Bot**
Choose input method:

1. Send `email@example.com` to get OTP
"
        "2. Or send your direct `accessToken` (starting with `FwOX...`) to continue"
    )

@bot.on_message(filters.text & ~filters.command("start"))
async def handle_input(client, message: Message):
    text = message.text.strip()

    if "@" in text and "." in text:
        # Assume email, send OTP
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.cdsjourney.in/api/v1/auth/otp", json={"email": text}) as r:
                if r.status == 200:
                    user_tokens[message.chat.id] = {"email": text}
                    await message.reply("OTP sent. Reply with the OTP.")
                else:
                    await message.reply("Failed to send OTP.")
    elif text.isdigit() and message.chat.id in user_tokens:
        # OTP verify
        email = user_tokens[message.chat.id]["email"]
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.cdsjourney.in/api/v1/auth/login", json={"email": email, "otp": text}) as r:
                res = await r.json()
                token = res.get("accessToken")
                if token:
                    user_tokens[message.chat.id]["token"] = token
                    await message.reply("Login successful! Send /extract to get Zoom links.")
                else:
                    await message.reply("Login failed.")
    elif text.startswith("FwOX"):
        user_tokens[message.chat.id] = {"token": text}
        await message.reply("Token saved! Send /extract to get Zoom links.")
    else:
        await message.reply("Unrecognized input.")

@bot.on_message(filters.command("extract"))
async def extract_links(client, message: Message):
    data = user_tokens.get(message.chat.id)
    if not data or "token" not in data:
        await message.reply("Please login first with email/OTP or token.")
        return

    token = data["token"]
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.cdsjourney.in/api/v1/purchased/batches", headers=headers) as r:
            res = await r.json()
            batches = res.get("data", [])
            if not batches:
                await message.reply("No batches found.")
                return
            text = "**Your Batches:**
"
            for i, b in enumerate(batches):
                text += f"{i+1}. {b.get('batchName')} (ID: {b.get('id')})
"
            await message.reply(text + "
Reply with batch ID to extract Zoom links.")
            user_tokens[message.chat.id]["batchlist"] = batches

@bot.on_message(filters.text & filters.reply)
async def batch_link_fetcher(client, message: Message):
    data = user_tokens.get(message.chat.id)
    if not data or "token" not in data or "batchlist" not in data:
        return

    try:
        batch_id = int(message.text.strip())
    except:
        await message.reply("Invalid batch ID.")
        return

    token = data["token"]
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.cdsjourney.in/api/v1/batches/{batch_id}/contents"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as r:
            res = await r.json()
            contents = res.get("data", [])
            links = []
            for c in contents:
                if "zoom" in c.get("url", ""):
                    links.append(c["url"])
            if links:
                file_path = f"/mnt/data/zoom_links_{batch_id}.txt"
                with open(file_path, "w") as f:
                    f.write("
".join(links))
                await message.reply_document(file_path)
            else:
                await message.reply("No Zoom links found.")

bot.run()
